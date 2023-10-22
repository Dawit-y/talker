from .forms import PostForm


def post_form(request):
    # Your form logic here
    form = PostForm()
    return {'post_form': form}