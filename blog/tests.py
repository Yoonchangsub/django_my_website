from django.test import TestCase , Client
from bs4 import BeautifulSoup

# Create your tests here.
from blog.models import Post
from django.utils import timezone
from django.contrib.auth.models import User


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith',password='nopassword')


    def test_post_list(self):
        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content ,'html.parser')

        title = soup.title
        

        print(title.text)
        self.assertEqual(title.text,'blog')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog',navbar.text)
        self.assertIn('About me',navbar.text)

        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다',soup.body.text)

        post_000 = Post.objects.create(
            title='The first Post',
            content='TESSSS',
            created = timezone.now(),
            author = self.author_000,
        )

        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다', soup.body)
        self.asserIn(post_000.title, soup.body)

    def test_post_detail(self):
        self.assertGreater(Post.objects.count(), 0)