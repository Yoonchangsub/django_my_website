from django.test import TestCase , Client
from bs4 import BeautifulSoup

# Create your tests here.
from blog.models import Post
from django.utils import timezone
from django.contrib.auth.models import User

def create_post(title , content , author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
    )

    return blog_post

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith',password='nopassword')

    def check_navbar(self,soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def test_post_list(self):
        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content ,'html.parser')

        title = soup.title
        

        print(title.text)
        self.assertEqual(title.text,'blog')

        self.check_navbar(soup)


        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다',soup.body.text)

        post_000 = create_post(
            title='The first Post',
            content='TESSSS',
            author=self.author_000,
        )

        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body

        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        self.assertIn(post_000.title, body.text)

    def test_post_detail(self):
        # todo Post 디테일에 대한 테스트 케이스 작성
        post_000 = create_post(
            title='The first Post',
            content='TESSSS',
            author=self.author_000,
        )
        self.assertGreater(Post.objects.count(), 0)
       # self.assertEqual(post_000.get_absolute_url(), '/blog/{}'.format(post_000.pk))
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))
        response = self.client.get(post_000_url)

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text , '{} - Blog'.format(post_000.title))

        self.check_navbar(soup)