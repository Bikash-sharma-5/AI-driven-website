# import json
# from rest_framework import viewsets, status
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.views import APIView
# from .forms import WebsiteForm
# import uuid
# from rest_framework.permissions import IsAuthenticated
# from .models import Website
# from .serializers import WebsiteSerializer

# # Prefilled website structure generator
# def generate_full_website_structure(business_type, industry):
#     return {
#         "home": {
#             "hero": {
#                 "heading": f"Welcome to {business_type} Experts!",
#                 "subheading": f"Providing excellence in the {industry} industry."
#             },
#             "about": f"We specialize in {business_type} services tailored to your needs in the {industry} sector."
#         },
#         "services": {
#             "title": "Our Services",
#             "items": [
#                 f"Professional {business_type} Consultation",
#                 f"{industry} Solutions Package"
#             ]
#         },
#         "contact": {
#             "email": f"info@{business_type.lower().replace(' ', '')}.com",
#             "phone": "+91 98765 43210",
#             "address": "123, Main Street, Your City"
#         },
#         "about": {
#             "title": "About Us",
#             "description": f"At {business_type} Experts, we are committed to delivering top-notch services in the {industry} industry with a customer-first approach."
#         }
#     }

# # Login View
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'builder/login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# # Register View
# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.objects.create_user(username=username, password=password)
#         login(request, user)
#         return redirect('dashboard')
#     return render(request, 'builder/register.html')

# @login_required
# def dashboard_view(request):
#     websites = Website.objects.filter(user_id=request.user.id)
#     return render(request, 'builder/dashboard.html', {'websites': websites})

# @login_required
# def create_website_view(request):
#     if request.method == 'POST':
#         form = WebsiteForm(request.POST)
#         if form.is_valid():
#             # Generate content
#             business_type = form.cleaned_data['business_type']
#             industry = form.cleaned_data['industry']
#             content = generate_full_website_structure(business_type, industry)

#             # Create and save the website with content
#             website = Website.objects.create(
#                 user_id=request.user.id,
#                 name=form.cleaned_data['name'],
#                 business_type=business_type,
#                 industry=industry,
#                 preview_token=uuid.uuid4()
#             )
#             website.set_generated_content(content)
#             website.save()

#             return redirect('dashboard')
#     else:
#         form = WebsiteForm()
#     return render(request, 'builder/create_website.html', {'form': form})

# # ViewSet for full CRUD & content generation
# class WebsiteViewSet(viewsets.ModelViewSet):
#     queryset = Website.objects.none()
#     serializer_class = WebsiteSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Website.objects.filter(user_id=self.request.user.id)

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user.id)

#     @action(detail=True, methods=['post'])
#     def generate_content(self, request, pk=None):
#         website = self.get_object()
#         content = generate_full_website_structure(website.business_type, website.industry)
#         website.set_generated_content(content)
#         website.save()

#         return Response({
#             "message": "Content generated successfully",
#             "generated_content": website.get_generated_content()
#         })

#     @action(detail=True, methods=['post'])
#     def update_content(self, request, pk=None):
#         website = self.get_object()
#         content = request.data.get("content")

#         if content:
#             website.set_generated_content(content)
#             website.save()
#             return Response({"message": "Website content updated."})
#         return Response({"error": "Content not provided."}, status=400)

#     @action(detail=True, methods=['post'])
#     def update_custom_content(self, request, pk=None):
#         website = self.get_object()
#         custom_content = request.data.get("custom_content")

#         if custom_content:
#             website.set_custom_content(custom_content)
#             website.save()
#             return Response({"message": "Custom content updated."})
#         return Response({"error": "Custom content not provided."}, status=400)

#     def destroy(self, request, *args, **kwargs):
#         website = self.get_object()
#         if website.user_id != request.user.id:
#             return Response({"error": "Not authorized to delete this website."}, status=403)
#         website.delete()
#         return Response({"message": "Website deleted successfully."}, status=204)

# class WebsiteCRUDView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         business_type = request.data.get("business_type")
#         industry = request.data.get("industry")
#         name = request.data.get("name")

#         content = generate_full_website_structure(business_type, industry)

#         website = Website.objects.create(
#             name=name,
#             business_type=business_type,
#             industry=industry,
#             user_id=request.user.id
#         )
#         website.set_generated_content(content)
#         website.save()

#         return Response({
#             "message": "Website created successfully",
#             "website": WebsiteSerializer(website).data,
#             "preview_url": request.build_absolute_uri(website.get_preview_url())
#         }, status=status.HTTP_201_CREATED)

# class PreviewWebsiteView(APIView):
#     def get(self, request, token):
#         website = get_object_or_404(Website, preview_token=token)
#         content = website.get_generated_content()

#         html = f"""
#         <html>
#         <head><title>{website.name}</title></head>
#         <body style="font-family:sans-serif;">
#             <h1>{content['home']['hero']['heading']}</h1>
#             <p>{content['home']['hero']['subheading']}</p>

#             <h2>About</h2>
#             <p>{content['about']['description']}</p>

#             <h2>Services</h2>
#             <ul>
#                 {''.join([f"<li>{item}</li>" for item in content['services']['items']])}
#             </ul>

#             <h2>Contact</h2>
#             <p>Email: {content['contact']['email']}</p>
#             <p>Phone: {content['contact']['phone']}</p>
#             <p>Address: {content['contact']['address']}</p>
#         </body>
#         </html>
#         """
#         return HttpResponse(html)

# def preview_website(request, token):
#     website = get_object_or_404(Website, preview_token=token)

#     if isinstance(website.generated_content, str):
#         content = json.loads(website.generated_content)
#     else:
#         content = website.generated_content

#     return render(request, "builder/preview.html", {"content": content})
# @login_required
# def preview_user_website(request, preview_token):
#     website = get_object_or_404(Website, preview_token=preview_token)

#     content = website.get_custom_content()
#     if not content:
#         content = website.get_generated_content()

#     print("✅ FINAL CONTENT TYPE:", type(content))
#     print("✅ FINAL CONTENT VALUE:", content)

#     return render(request, 'nok/preview.html', {'content': content})

# @login_required
# def delete_website(request, website_id):
#     website = get_object_or_404(Website, preview_token=website_id, user_id=request.user.id)

#     if request.method == 'POST':
#         website.delete()
#         return redirect('dashboard')  # or wherever your dashboard view is
#     return redirect('dashboard')

import json
import uuid
import requests
from rest_framework import viewsets, status
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.conf import settings
from .forms import WebsiteForm
from .models import Website
from rest_framework.permissions import IsAuthenticated
from .serializers import WebsiteSerializer
from pymongo import MongoClient

HF_API_KEY = settings.HUGGINGFACE_API_KEY

# Hugging Face Text Generation
def generate_text(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers=headers,
        json=payload
    )
    result = response.json()
    return result[0]['generated_text'] if isinstance(result, list) and 'generated_text' in result[0] else "Content coming soon..."

# Generate full website content
def generate_full_website_structure(business_type, industry):
    heading = generate_text(f"Write a captivating and unique hero heading for a {business_type} in the {industry} industry.")
    subheading = generate_text(f"Write an engaging 2-line hero subheading that explains what a {business_type} in the {industry} industry offers.")

    about = generate_text(f"Write a detailed About Us section for a {business_type} working in the {industry} industry. Mention the mission, goals, and unique values.")

    services_raw = generate_text(f"List and describe 4 services that a {business_type} typically offers in the {industry} industry. Write in bullet points or short paragraphs.")
    services = [s.strip("-• ") for s in services_raw.split("\n") if s.strip()]

    testimonials = [
        generate_text(f"Write a short testimonial from a satisfied customer of a {business_type} in the {industry} industry."),
        generate_text(f"Write another testimonial that praises the quality and professionalism of a {business_type} in the {industry} sector.")
    ]

    call_to_action = generate_text(f"Write a compelling call to action encouraging users to get in touch with a {business_type} in the {industry} industry.")

    return {
        "home": {
            "hero": {
                "heading": heading,
                "subheading": subheading
            },
            "about": about,
            "cta": call_to_action
        },
        "services": {
            "title": "Our Services",
            "items": services
        },
        "testimonials": testimonials,
        "contact": {
            "email": f"contact@{business_type.lower().replace(' ', '')}.com",
            "phone": "+91 98765 43210",
            "address": "123 Business Park, Industrial Zone, Your City"
        },
        "about": {
            "title": "About Us",
            "description": about
        }
    }

# Login, logout, register views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'builder/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        login(request, user)
        return redirect('dashboard')
    return render(request, 'builder/register.html')

@login_required
def dashboard_view(request):
    websites = Website.objects.filter(user_id=request.user.id)
    return render(request, 'builder/dashboard.html', {'websites': websites})

@login_required
def create_website_view(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            business_type = form.cleaned_data['business_type']
            industry = form.cleaned_data['industry']
            content = generate_full_website_structure(business_type, industry)

            website = Website.objects.create(
                user_id=request.user.id,
                name=form.cleaned_data['name'],
                business_type=business_type,
                industry=industry,
                preview_token=uuid.uuid4()
            )
            website.set_generated_content(content)
            website.save()

            return redirect('dashboard')
    else:
        form = WebsiteForm()
    return render(request, 'builder/create_website.html', {'form': form})

class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.none()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Website.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=['post'])
    def generate_content(self, request, pk=None):
        website = self.get_object()
        content = generate_full_website_structure(website.business_type, website.industry)
        website.set_generated_content(content)
        website.save()
        return Response({
            "message": "Content generated successfully",
            "generated_content": website.get_generated_content()
        })

    @action(detail=True, methods=['post'])
    def update_content(self, request, pk=None):
        website = self.get_object()
        content = request.data.get("content")
        if content:
            website.set_generated_content(content)
            website.save()
            return Response({"message": "Website content updated."})
        return Response({"error": "Content not provided."}, status=400)

    @action(detail=True, methods=['post'])
    def update_custom_content(self, request, pk=None):
        website = self.get_object()
        custom_content = request.data.get("custom_content")
        if custom_content:
            website.set_custom_content(custom_content)
            website.save()
            return Response({"message": "Custom content updated."})
        return Response({"error": "Custom content not provided."}, status=400)

    def destroy(self, request, *args, **kwargs):
        website = self.get_object()
        if website.user_id != request.user.id:
            return Response({"error": "Not authorized to delete this website."}, status=403)
        website.delete()
        return Response({"message": "Website deleted successfully."}, status=204)

class WebsiteCRUDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        business_type = request.data.get("business_type")
        industry = request.data.get("industry")
        name = request.data.get("name")
        content = generate_full_website_structure(business_type, industry)

        website = Website.objects.create(
            name=name,
            business_type=business_type,
            industry=industry,
            user_id=request.user.id
        )
        website.set_generated_content(content)
        website.save()

        return Response({
            "message": "Website created successfully",
            "website": WebsiteSerializer(website).data,
            "preview_url": request.build_absolute_uri(website.get_preview_url())
        }, status=status.HTTP_201_CREATED)

class PreviewWebsiteView(APIView):
    def get(self, request, token):
        website = get_object_or_404(Website, preview_token=token)
        content = website.get_generated_content()

        html = f"""
        <html>
        <head><title>{website.name}</title></head>
        <body style="font-family:sans-serif;">
            <h1>{content['home']['hero']['heading']}</h1>
            <p>{content['home']['hero']['subheading']}</p>

            <h2>About</h2>
            <p>{content['about']['description']}</p>

            <h2>Services</h2>
            <ul>{''.join([f"<li>{item}</li>" for item in content['services']['items']])}</ul>

            <h2>Testimonials</h2>
            <ul>{''.join([f"<li>“{t}”</li>" for t in content['testimonials']])}</ul>

            <h2>Contact</h2>
            <p>Email: {content['contact']['email']}</p>
            <p>Phone: {content['contact']['phone']}</p>
            <p>Address: {content['contact']['address']}</p>

            <h2>Get in Touch</h2>
            <p>{content['home']['cta']}</p>
        </body>
        </html>
        """
        return HttpResponse(html)

def preview_website(request, token):
    website = get_object_or_404(Website, preview_token=token)
    content = website.get_generated_content() if isinstance(website.generated_content, dict) else json.loads(website.generated_content)
    return render(request, "builder/preview.html", {"content": content})

@login_required
def preview_user_website(request, preview_token):
    website = get_object_or_404(Website, preview_token=preview_token)
    content = website.get_custom_content() or website.get_generated_content()
    return render(request, 'nok/preview.html', {'content': content})

@login_required
def delete_website(request, website_id):
    website = get_object_or_404(Website, preview_token=website_id, user_id=request.user.id)
    if request.method == 'POST':
        website.delete()
    return redirect('dashboard')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from builder.models import Website
import json
from pymongo import MongoClient

@login_required
def update_content_view(request, website_id):
    website = get_object_or_404(Website, id=website_id, user_id=request.user.id)

    if request.method == 'POST':
        # Get all form data
        hero_heading = request.POST.get('hero_heading', '')
        hero_subheading = request.POST.get('hero_subheading', '')
        about_description = request.POST.get('about_description', '')
        cta_text = request.POST.get('cta_text', '')

        service_items = [item.strip() for item in request.POST.get('service_items', '').split(',') if item.strip()]
        testimonials = [item.strip() for item in request.POST.get('testimonials', '').split(',') if item.strip()]

        contact_email = request.POST.get('contact_email', '')
        contact_phone = request.POST.get('contact_phone', '')
        contact_address = request.POST.get('contact_address', '')

        business_type = website.business_type  # use this for default fallback if needed

        # Construct content dictionary
        updated_content = {
            "home": {
                "hero": {
                    "heading": hero_heading,
                    "subheading": hero_subheading
                },
                "about": about_description,
                "cta": cta_text
            },
            "services": {
                "title": "Our Services",
                "items": service_items
            },
            "testimonials": testimonials,
            "contact": {
                "email": contact_email or f"contact@{business_type.lower().replace(' ', '')}.com",
                "phone": contact_phone or "+91 98765 43210",
                "address": contact_address or "123 Business Park, Industrial Zone, Your City"
            },
            "about": {
                "title": "About Us",
                "description": about_description
            }
        }

        # Save updated content to generated_content field
        website.set_generated_content(updated_content)
        website.save()
        return redirect('dashboard')

    # GET method - show existing content
    return render(request, 'builder/update_content.html', {
        'website': website,
        'content': website.get_generated_content()
    })