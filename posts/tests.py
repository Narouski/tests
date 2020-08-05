from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Post, User


class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='sarah',
            email='connor.s@skynet.com',
            password='12345'
        )
        self.post = Post.objects.create(
            text="You're talking about things "
                 "I haven't done yet in the past tense."
                 "It's driving me crazy!",
            author=self.user
        )

    def test_profile(self):
        response = self.client.get(
            reverse('profile',
                    kwargs={'username': self.post.author})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertIsInstance(response.context['author'], User)
        self.assertEqual(
            response.context['author'].username,
            self.user.username
        )

    def test_no_name(self):
        response = self.client.post(
            reverse('new'),
            data={'text': 'test'}
        )
        posts = Post.objects.all()
        for post in posts:
            self.assertNotEqual(post.text, "test")
        self.assertRedirects(
            response,
            "/auth/login/?next=/new/",
            302
        )

    def test_post_publication(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text='text',
            author=self.user
        )
        for url in {
            reverse('index'),
            reverse(
                'profile',
                kwargs={'username': self.user.username}
            ),
            reverse(
                'post',
                kwargs={'username': self.user.username,
                        'post_id': post.id}
            )
        }:
            response = self.client.get(url)
            self.assertContains(response, post.text)
            self.assertContains(response, post.author)

    def test_post_edit(self):
        post = Post.objects.create(
            text='old text in post',
            author=self.user,
        )
        edit_urls_list = [
            reverse('index'),
            reverse('profile',
                    kwargs={'username': self.user.username}),
            reverse('post',
                    kwargs={'username': self.user.username,
                            'post_id': post.id})
        ]
        for url in edit_urls_list:
            new_text = 'This is text after edit.'
            response = self.client.post(
                url,
                data={'text': new_text}
            )
            self.assertEqual(response.status_code, 200)

    def test_page_404(self):
        test_page = self.client.get('/baba/', kwargs={'username': self.user.username})
        self.assertEqual(test_page.status_code, 404)

    def tearDown(self) -> None:
        print('The end')

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
def test_add_image(self):
    text = 'post with file not image'
    file_mock = mock.MagicMock(spec=File, name='copy.txt')
    response = self.client_auth.post(reverse('new_post'), data={
        'author': self.user,
        'group': self.group.pk,
        'text': text,
        'image': file_mock
        })
    self.assertFormError(response,
                         form='form',
                         field='image',
                         errors='Загрузите правильное изображение.'
                                ' Файл, который вы загрузили,'
                                ' поврежден или не является изображением.')
