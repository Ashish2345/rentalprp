from .models import Post
from django.views import generic


#for postlist views
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blogHome.html'


#for deatilview views
class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/blogDetail.html'
