from django.test import TestCase , Client
from bs4 import BeautifulSoup

# Create your tests here.
from blog.models import Post


class TestView(TestCase):

    def setUp(self):
        self.client = Client()


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