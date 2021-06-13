from django.test import TestCase
from core.models import Box, BoxVersion
from django.contrib.auth.models import User

# Create your tests here.
class BoxTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="user1")
        box = Box.objects.create(
            name="box1", creator=user, description="box with no downloads", 
            public=False
        )
        box_version = BoxVersion.objects.create(
            box=box, name="v1", kind="lv", description="example",
        )

    def test_box_downloads(self):
        """Test if the number of downloads starts as zero."""
        box = Box.objects.get(name="box1")
        self.assertEqual(box.downloads, 0)

    def test_box_version_path(self):
        """Test the filepath."""
        box_version = BoxVersion.objects.get(name="v1")
        self.assertEqual(box_version.box_version_path("ubuntu.iso"), "boxes/box1/box1-v1.box")

