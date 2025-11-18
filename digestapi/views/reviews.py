from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from digestapi.models import Review, Book


class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "book", "user", "rating", "comment", "created_at", "is_owner"]
        read_only_fields = ["user"]

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context["request"].user == obj.user


class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Get all reviews
        reviews = Review.objects.all()
        # Serialize the objects, and pass request to determine owner
        serializer = ReviewSerializer(reviews, many=True, context={"request": request})

        # Return the serialized data with 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Create a new instance of a review and assign property
        # values from the request payload using `request.data`
        comment = request.data.get("comment")
        rating = request.data.get("rating")
        book_id = request.data.get("book_id")

        # Get the Book instance
        book = Book.objects.get(pk=book_id)

        # Save the review
        review = Review.objects.create(
            user=request.user, 
            book=book, 
            comment=comment, 
            rating=rating
        )

        try:
            # Serialize the objects, and pass request as context
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the serialized data with 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)

            # Serialize the object (make sure to pass the request as context)
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the review with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)

            # Check if the user has permission to delete
            self.check_object_permissions(request, review)
            # Will return 403 if authenticated user is not author

            # Delete the review
            review.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
