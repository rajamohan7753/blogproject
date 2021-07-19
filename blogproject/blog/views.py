from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . forms import EmailPostForm,CommentForm,signupform
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from taggit.models import Tag

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def post_list(request,tag_slug=None):
    object_list= Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator= Paginator(object_list,1)
    page = request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'page':page,'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post, status='published',
                             publish__year=year,publish__month=month,
                            publish__day=day )
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form})


def post_share(request,post_id):
    post= get_object_or_404(Post,id=post_id,status='published')
    sent= False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd= form.cleaned_data

            post_url= request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s  comments: {cd['comments:']}"
            send_mail(subject,message,'k.rajamohanreddy99@gmail.com', [cd['to']])
            send = True

    else:
        form = EmailPostForm()
    return render(request,'blog/post_share.html',{'post':post,'form ':form ,'sent':sent})

def logout_view(request):

    return render(request,'blog/post/logout.html')


def registerpage(request):

    form=signupform()
    if request.method=='POST':
        form=signupform(request.POST)
        user=form.save()
        user.set_password(user.password)
        user.save()
        return redirect('post')




    context = {'form':form}
    return render(request,'registration/signup.html',context)


def loginpage(request):

    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('post')
    return render(request,'registration/login.html')
