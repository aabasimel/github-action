from django.test import TestCase
from .models import Post
# Create your tests here.
class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            body="Test post content"


        )
    def test_post_creation(self):
        post=Post.objects.get(id=1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.body, 'Test post contect')

    
    def test_post_created_auto_now_add(self):
        post=Post.objects.get(id=1)
        self.assertEqual(post.created)