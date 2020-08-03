from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from .models import Group, Post, User


class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='sarah',
            email='connor.s@skynet.com',
            password='12345'
        )
        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense."
                 "It's driving me crazy!",
            author=self.user
        )

    def test_profile(self):
        response = self.client.get(reverse('profile',
                                           kwargs={'username': self.post.author}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertIsInstance(response.context['author'], User)
        self.assertEqual(response.context['author'].username, self.user.username)

    def test_no_name(self):
        response = self.client.post(reverse('new'), data={'text': 'test'})
        posts = Post.objects.all()
        for post in posts:
            self.assertNotEqual(post.text, "test")
        self.assertRedirects(response, "/auth/login/?next=/new/", 302)

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

    def tearDown(self) -> None:
        print('The end')
