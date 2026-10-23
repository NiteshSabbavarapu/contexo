from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .embeddings import generate_embedding
from .serializers import DocumentSerializer
from .models import DocumentChunk
from .chunking import split_into_chunks
from .serializers import SearchSerializer
from .generation import generate_answer
from .hybrid_search import hybrid_search


@api_view(["POST"])
def create_document(request):
    serializer = DocumentSerializer(data=request.data)

    if serializer.is_valid():
        document = serializer.save()

        chunks = split_into_chunks(document.content)

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            DocumentChunk.objects.create(
                document=document,
                content=chunk,
                chunk_index=index,
                embedding=embedding,
            )

        return Response(
            {
                "document": DocumentSerializer(document).data,
                "chunks_created": len(chunks)
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def search_documents(request):
    serializer = SearchSerializer(data=request.data)

    if serializer.is_valid():
        question = serializer.validated_data["question"]
        chunks = hybrid_search(question)
        answer = generate_answer(question, chunks)

        sources = [
            {
                "document": chunk.document.title,
                "content": chunk.content,
            }
            for chunk in chunks
        ]

        return Response(
            {
                "question": question,
                "answer": answer,
                "sources": sources,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
