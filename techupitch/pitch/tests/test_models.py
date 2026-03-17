from django.test import TestCase

from pitch.models import Player

class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Player.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_birth_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'birth')

    def test_first_name_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        player = Player.objects.get(id=1)
        expected_object_name = f'{player.last_name}, {player.first_name}'
        self.assertEqual(str(player), expected_object_name)

    def test_get_absolute_url(self):
        player = Player.objects.get(id=1)
        # This will also fail if the URLConf is not defined.
        self.assertEqual(player.get_absolute_url(), '/pitch/player/1')