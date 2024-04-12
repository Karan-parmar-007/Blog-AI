from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Category, Like, AnonymousPost
from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm, SummaryForm, AnonymousPostForm
from django.utils import timezone
import csv
from django.core.paginator import Paginator
from googletrans import Translator
from django.db.models import Count
from .utils import generate_random_string
from django.shortcuts import render, get_object_or_404
import os
import pyttsx3
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


def get_blog(post_content):

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])    
    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path="C:\\coding\\blog_ai\\blog_ai\\llm_model\\final-lawyer-llm.gguf",
        temperature=0.8,
        max_tokens=5000000,
        top_p=1,
        n_ctx=4096,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    

# Template that includes placeholders for instruction, input, and the desired output format
    prompt = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    Generate a blog for this summary of around 1000 words

    ### Input:
    {post_content}

    ### Response:
    """
        


    response=llm.invoke(prompt.format(post_content=post_content))

    
    return response


def get_summary(post_content):

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])    
    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path="C:\\coding\\blog_ai\\blog_ai\\llm_model\\final-lawyer-llm.gguf",
        temperature=0.8,
        max_tokens=5000000,
        top_p=1,
        n_ctx=4096,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    

# Template that includes placeholders for instruction, input, and the desired output format
    prompt = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    Generate a detailed summary for this blog post around 500 words

    ### Input:
    {post_content}

    ### Response:
    """
        


    response=llm.invoke(prompt.format(post_content=post_content))

    
    return response


def get_script(post_content):

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])    
    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path="C:\\coding\\blog_ai\\blog_ai\\llm_model\\final-lawyer-llm.gguf",
        temperature=0.8,
        max_tokens=5000000,
        top_p=1,
        n_ctx=4096,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    

# Template that includes placeholders for instruction, input, and the desired output format
    prompt = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    Generate a script for a youtube video for this post of around 2000 words. The script must be more than 2000 words strict.

    ### Input:
    {post_content}

    ### Response:
    """
        


    response=llm.invoke(prompt.format(post_content=post_content))

    
    return response


def get_llama_response(post_content):

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])    
    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path="C:\\coding\\blog_ai\\blog_ai\\llm_model\\final-lawyer-llm.gguf",
        temperature=0.8,
        max_tokens=5000000,
        top_p=1,
        n_ctx=4096,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    

# Template that includes placeholders for instruction, input, and the desired output format
    prompt = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    Reframe what I am sending you in a blog and as long as possible 

    ### Input:
    {post_content}

    ### Response:
    """
        


    response=llm.invoke(prompt.format(post_content=post_content))
    print("answer generated")
    
    return response



def create_post(request):

    categories = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.user_id = request.user

            # Get the post content
            post_content = form.cleaned_data['content']
            
            # Read bad words from CSV file
            bad_words = set()
            with open('English.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    bad_words.update(row)

            # Check for bad words
            has_bad_words = any(word in post_content for word in bad_words)
            if has_bad_words:
                post_content = get_llama_response(post_content)
                
                # Redirect user to create a new post with the updated content
                return render(request, 'new_post.html', {'form': form, 'post_content': post_content})

            # Save the post with original content
            post.content = post_content
            post.save()

            return redirect('mainhome')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form, 'categories': categories})




def home(request):
    posts = Post.objects.all().order_by('-created_at')[:4]
    posts_with_videos = Post.objects.filter(video_file__isnull=False).order_by('-created_at')[:4]
    anoy_posts = AnonymousPost.objects.filter(is_valid=True).order_by('-created_at')[:4]
    top_liked_posts = Post.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:3]

    comments_number_post = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4]

    categories = Category.objects.all()
    return render(request, 'home.html', {'posts': posts, 'categories': categories, 'posts_with_videos':posts_with_videos, 'comments_number_post':comments_number_post, 'top_liked_posts':top_liked_posts, 'anoy_posts': anoy_posts})



# Create your views here.




def particularcategory(request, category_name):

    category = get_object_or_404(Category, title=category_name)
    posts = Post.objects.filter(cat=category).order_by('-created_at')
    categories = Category.objects.all()
    title = request.GET.get('title')
    if title != '' and title is not None:
        posts = posts.filter(title__icontains=title)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    return render(request, 'posts_by_category.html', {'posts': posts, 'categories': categories})


def userpost(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(user_id=request.user).order_by('-created_at')
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'user_post.html', {'posts':posts, 'categories': categories})


def editpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Check if the current user is the author of the post
    if request.user != post.user_id:
        # If not, redirect to some other page or show an error message
        return redirect('mainhome')  # Redirect to home page

    # If user is the author, process the edit form
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('userpost')  # Redirect to user's posts page
    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {'form': form})




def specificpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    categories = Category.objects.all()
    is_liked = False
    form = CommentForm()
    # Check if the user is authenticated for likes
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()

    translated_content = None
    if request.method == 'POST':
        target_language = request.POST.get('target_language')
        translated_content = translate_content(post.content, target_language)
        if translated_content:
            post.translated_content = translated_content  # Store translated content in post object

    # Render the specificpost.html template with the post and other context data
    return render(request, "specificpost.html", {
        'post': post, 
        'comments': comments, 
        'categories': categories, 
        'is_liked': is_liked,
        'translated_content': translated_content,
        'form': form,  # Pass translated content to the template using the correct variable name
    })


def generate_summary(request):
    if request.method == 'POST':
        categories = Category.objects.all()
        post_content = request.POST.get('post_content')
        summary = get_summary(post_content)  # Call function to generate summary
        # Render the summary directly in the template
        return render(request, 'generated_summary.html', {'summary': summary, 'categories': categories})

def generate_script(request):
    if request.method == 'POST':
        categories = Category.objects.all()
        post_content = request.POST.get('post_content')
        script = get_script(post_content)  # Call function to generate video script
        # Render the script directly in the template
        return render(request, 'generated_script.html', {'script': script, 'categories': categories})
    
def generate_blog(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            summary = form.cleaned_data['summary']
            blog_content = get_blog(summary)  # Call function to generate blog post
            return render(request, 'generate_blog.html', {'blog_content': blog_content, 'categories': categories, 'form': form})
    else:
        form = SummaryForm()
        return render(request, 'generate_blog.html', {'categories': categories, 'form': form})
    


def like_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()  # Unlike the post if already liked
    return redirect('specificpost', post_id=post_id)


# views.py

def translate_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    categories = Category.objects.all()
    is_liked = False

    # Check if the user is authenticated for likes
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
 # Store translated content in post object

    # Render the specificpost.html template with the post and other context data


    if request.method == 'POST':
        if request.user.is_authenticated:
            is_liked = Like.objects.filter(user=request.user, post=post).exists()
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all().order_by('-created_at')
        categories = Category.objects.all()
        is_liked = False
        target_language = request.POST.get('target_language')
        new_content = post.content
        translated_contentt = translate_content(new_content, target_language)

        return render(request, "specificpost.html", {
            'post': post, 
            'comments': comments, 
            'categories': categories, 
            'is_liked': is_liked,
            'translated_contentt': translated_contentt,  # Pass translated content to the template
        })    
    else:
            # Handle translation failure
        pass
    return redirect('specificpost', post_id=post_id)

def translate_content(content, target_language):
    translator = Translator()
    try:
        translation = translator.translate(content, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def index_post(request):
    return redirect('index.html')

def create_anonymous_post(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = AnonymousPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Validate CAPTCHA
            captcha_entered = form.cleaned_data['captcha']
            captcha_generated = request.session.get('captcha_text')
            if captcha_entered != captcha_generated:
                # CAPTCHA mismatch
                return render(request, 'incorrect_captcha.html', {'categories':categories})

            form.save()
            return redirect('mainhome')  
    else:
        form = AnonymousPostForm()
        captcha_text = generate_random_string()
        request.session['captcha_text'] = captcha_text

    return render(request, 'create_anonymous_post.html', {'form': form, 'categories': categories, 'captcha_text': captcha_text})



def anonymous_post_list(request):
    posts = AnonymousPost.objects.filter(is_valid=True).order_by('-created_at')
     
    categories = Category.objects.all()
    title = request.GET.get('title')
    if title != '' and title is not None:
        posts = posts.filter(title__icontains=title)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # return render(request, 'anonymous_post_list.html', {'posts': posts})
    return render(request, 'anonymous_post_list.html', {'posts': posts, 'categories': categories})

def anonymous_post_detail(request, post_id):
    post = get_object_or_404(AnonymousPost, pk=post_id)
    categories = Category.objects.all()
    title = request.GET.get('title')
    if title != '' and title is not None:
        posts = posts.filter(title__icontains=title)

    return render(request, 'anonymous_post_detail.html', {'post':post, 'categories': categories})




engine = pyttsx3.init()

def read_text(request):
    if request.method == 'POST':
        # Get the text to be read from the POST request
        text = request.POST.get('text', '')
        if text:
            # Set properties for the voice (adjust as needed)
            rate = int(request.POST.get('rate', 150))  # Default rate: 150 words per minute
            volume = float(request.POST.get('volume', 0.9))  # Default volume: 0.9 (90%)

            # Set voice properties
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)  # Select a voice (female voice in this case)
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)

            # Add the text to be spoken
            engine.say(text)

            # Block until the text is spoken
            engine.runAndWait()

            return HttpResponse("Text read successfully.")
        else:
            return HttpResponse("Error: Text not provided in the request.", status=400)
    else:
        return HttpResponse("Error: Only POST requests are allowed.", status=405)
    
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment object but don't save it yet
            new_comment = form.save(commit=False)
            # Associate the comment with the post
            new_comment.post_id = post_id
            # Associate the comment with the logged-in user (if authenticated)
            if request.user.is_authenticated:
                new_comment.user_id = request.user
            # Save the comment to the database
            new_comment.save()
    # Redirect back to the same page after comment submission
    return redirect('specificpost', post_id=post_id)