from django.shortcuts import render, redirect
from orders.models import Order
from django.contrib import messages
from django.shortcuts import get_object_or_404
from dynamic_ui.models import Profile as Page, PageImage, PageVideo
import os


def check_image_exists_then_delete(image_id):
    try:
        PageImage.objects.get(id=image_id)
        PageImage.objects.get(id=image_id).delete()
        return True
    except PageImage.DoesNotExist:
        return False


def check_video_exists_then_delete(video_id):
    try:
        PageVideo.objects.get(id=video_id)
        PageVideo.objects.get(id=video_id).delete()
        return True
    except PageVideo.DoesNotExist:
        return False


dashboard_page_data = {
    "images": [
        {
            "id": 1,
            "path": "page_images/1.jpg",
        },
        {
            "id": 2,
            "path": "page_images/2.jpg",
        },
    ],
    "heading1": "Explore Gupta Rudraksha",
    "description1": "Dive deep with us in our Gupta Rudraksha Journey and our get to know us even more better.",
    "video_link1": "https://youtu.be/_drMO01Mjtc?si=cKWZvFp3SgaL8ttV",
    "heading2": "Our Sacred Commitment",
    "description2": "Certified Excellence in Rudraksha - Nepal's Premier ISO 9001:2015 Accredited Organization",
    "header9": "Exclusive and Rare Rudraksha Collection at Gupta Rudraksha ®️",
    "description6": "Discover the exclusive and rare Rudraksha collection only at Gupta Rudraksha. Our lab-certified, high-quality beads channel ancient spiritual energies for peace, prosperity, and personal growth. Each bead is meticulously chosen to ensure authenticity and potency, providing powerful benefits. Experience genuine, transformative spiritual tools to enhance your life&apos;s journey with Gupta Rudraksha.",
    "image1": {
        "id": 1,
        "path": "page_images/1.jpg",
    },
    "org_item": [
        {
            "title": "Since 1973",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Vedic Energization",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Lab Certification",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "ISO 9001:2015 certified",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Secure Payment",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
    ],
    "heading3": "Discover Your Path",
    "heading4": "Astrology-Guided Personal Growth",
    "description3": "Unlock your potential with our expert-led consultations and sacred Rudraksha beads.",
    "discover_item": [
        {
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "title": "Spirituality",
        },
        {
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "title": "Meditation",
        },
        {
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "title": "Wellness",
        },
    ],
    "heading5": "Nepal's 1st & only",
    "heading6": "ISO Certified",
    "heading7": "Rudraksha Organization",
    "description5": "Explore the largest collection of authentic Gupta Rudraksha energized as per our vedic process. For nearly 3+ generations Gupta Rudraksha has been the pioneer of Rudraksha and Shaligram and has supported millions of devotees attain spiritual and professional goals.",
    "heading8": "Gupta Rudraksha - The Only Vendor in the World To 100% Lifetime Money Back Authenticity Guarantee.",
    "footer_image1": {
        "id": 1,
        "path": "page_images/1.jpg",
    },
    "footer_image2": {
        "id": 1,
        "path": "page_images/1.jpg",
    },
}


def dashboard_page(request):
    page = Page.objects.filter(page_name="dashboard").first()

    if not page:
        page = Page(
            page_name="dashboard",
            data=dashboard_page_data,
        )
        page.save()
    if request.method == "POST":
        print(request.POST)
        if request.FILES.get("images"):
            # Delete the existing image
            existing_images = page.data.get("images")
            if existing_images:
                for image in existing_images:
                    check_image_exists_then_delete(image["id"])

            # Save the new image
            page.data["images"] = []
            for image in request.FILES.getlist("images"):
                page_image = PageImage(page=page, image=image)
                page_image.save()
                page.data["images"].append(
                    {
                        "id": page_image.id,
                        "path": page_image.image.url,
                    }
                )
        if request.FILES.get("footer_image1"):
            check_image_exists_then_delete(page.data["footer_image1"]["id"])
            page_image = PageImage(page=page, image=request.FILES.get("footer_image1"))
            page_image.save()
            page.data["footer_image1"] = {
                "id": page_image.id,
                "path": page_image.image.url,
            }
        if request.FILES.get("footer_image2"):
            check_image_exists_then_delete(page.data["footer_image2"]["id"])
            page_image = PageImage(page=page, image=request.FILES.get("footer_image2"))
            page_image.save()
            page.data["footer_image2"] = {
                "id": page_image.id,
                "path": page_image.image.url,
            }
        if request.FILES.get("image1"):
            ## key is not exist then create
            if "image1" not in page.data:
                page.data["image1"] = {
                    "id": 1,
                    "path": "page_images/1.jpg",
                }
            check_image_exists_then_delete(page.data["image1"]["id"])
            page_image = PageImage(page=page, image=request.FILES.get("image1"))
            page_image.save()

            page.data["image1"] = {
                "id": page_image.id,
                "path": page_image.image.url,
            }

        # Update Org Images and title
        for i in range(1, 6):
            image_key = f"org_title.{i}.image"
            title_key = f"org_title.{i}"
            if request.FILES.get(image_key):
                check_image_exists_then_delete(
                    page.data.get("org_item")[i - 1]["image"]["id"]
                )
                page_image = PageImage(page=page, image=request.FILES.get(image_key))
                page_image.save()
                page.data["org_item"][i - 1]["image"] = {
                    "id": page_image.id,
                    "path": page_image.image.url,
                }
            if request.POST.get(title_key):
                page.data["org_item"][i - 1]["title"] = request.POST.get(title_key)
        ## Update discover_item
        for i in range(1, 4):
            image_key = f"discover.{i}.image"
            title_key = f"discover.{i}"
            if request.FILES.get(image_key):
                check_image_exists_then_delete(
                    page.data.get("discover_item")[i - 1]["image"]["id"]
                )
                page_image = PageImage(page=page, image=request.FILES.get(image_key))
                page_image.save()
                page.data["discover_item"][i - 1]["image"] = {
                    "id": page_image.id,
                    "path": page_image.image.url,
                }
            if request.POST.get(title_key):
                page.data["discover_item"][i - 1]["title"] = request.POST.get(title_key)
                ## Check header then update
        for key, value in dashboard_page_data.items():
            if key.startswith("heading"):
                page.data[key] = request.POST.get(key)
        ## check description then update
        for key, value in dashboard_page_data.items():
            if key.startswith("description"):
                page.data[key] = request.POST.get(key)
        ## check video url
        if request.POST.get("video_link1"):
            page.data["video_link1"] = request.POST.get("video_link1")

        page.save()
    return render(
        request,
        "pages/dashboard.html",
        {"page": page.data},
    )


CONSULTATION_PAGE = "consultation"

consultation_page_data = {
    "header1": "Why Choose Our Consultation?",
    "description1": "Gain expert insights and personalized guidance.",
    "header_quote1": "Expert guidance from experienced professionals",
    "header_quote2": "Tailored advice for your specific needs",
    "header_quote2": "Tailored advice for your specific needs",
    "header_quote3": "Unlock clarity and direction in life",
    "header_quote4": "Free initial text-based consultation",
    "header2": "Personalized Rudraksha Consultation for Your Sacred Journey",
    "description2": "Whether you seek clarity on selecting the right Rudraksha for your spiritual goals or a deeper understanding of the sacred beads, our consultations are crafted to provide you with the wisdom and direction you seek .",
    "header3": "Three Generations of Expertise",
    "video_link1": "https://youtu.be/_drMO01Mjtc?si=LtWgP3Q9pf_RUdGe",
    "header4": "Who Should Book A Consultation?",
    "consultation_reasons": [
        {
            "title": "Personal Growth Seekers",
            "description": "Enhance personal growth, gain clarity, and overcome obstacles.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Business Owners and Entrepreneurs",
            "description": "Scale your business, improve operations, and navigate challenges.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Professionals Seeking Career Development",
            "description": "Plan your career, enhance job search strategies, and build professional skills.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Individuals Facing Life Transitions",
            "description": "Navigate significant life changes and find new directions for personal fulfillment.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Health and Wellness Enthusiasts",
            "description": "Optimize health, wellness, and live a balanced lifestyle.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Individuals Seeking Relationship Support",
            "description": "Resolve conflicts, improve communication, and build healthier relationships.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Financial Planning and Wealth Management",
            "description": "Optimize finances, plan for retirement, and grow wealth.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Anyone Seeking Clarity and Direction",
            "description": "Overcome feeling stuck, gain perspective, and find purpose.",
            "image": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
    ],
    "header5": "Perks of Consulting an Expert",
    "perks": [
        {
            "title": "Expert Guidance",
            "description": "Consultation provides access to expert advice and guidance from professionals who have in-depth knowledge and experience in their respective fields. We can offer valuable insights, strategies, and solutions tailored to your specific needs.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Mantras For You",
            "description": "Rudraksha experts can recommend specific mantras that align with your spiritual goals and intentions. Mantras are considered powerful tools for spiritual growth, and the right mantra can enhance the effectiveness of your Rudraksha.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Your Birth Chart",
            "description": "Rudraksha experts may also have knowledge of Vedic astrology. By analyzing your birth chart, they can provide insights into the planetary influences on your life and suggest Rudraksha combinations that may help balance and harmonize these influences.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Your Family Birth Chart",
            "description": "Understanding the birth charts of family members can offer a holistic view of the energy dynamics within the family. Rudraksha experts can provide guidance on selecting Rudraksha beads that complement the energy of the entire family, fostering a harmonious environment.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Pooja Service Recommendation",
            "description": "Understanding the birth charts of family members can offer a holistic view of the energy dynamics within the family. Rudraksha experts can provide guidance on selecting Rudraksha beads that complement the energy of the entire family, fostering a harmonious environment.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
        {
            "title": "Client Confidentiality",
            "description": "Understanding the birth charts of family members can offer a holistic view of the energy dynamics within the family. Rudraksha experts can provide guidance on selecting Rudraksha beads that complement the energy of the entire family, fostering a harmonious environment.",
            "image1": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
            "image2": {
                "id": 1,
                "path": "page_images/1.jpg",
            },
        },
    ],
}


def consultation_page(request):
    page = Page.objects.filter(page_name=CONSULTATION_PAGE).first()

    if not page:
        page = Page(
            page_name=CONSULTATION_PAGE,
            data=consultation_page_data,
        )
        page.save()
    if request.method == "POST":
        ## Check header then update
        for key, value in consultation_page_data.items():
            if key.startswith("header"):
                page.data[key] = request.POST.get(key)
        ## check description then update
        for key, value in consultation_page_data.items():
            if key.startswith("description"):
                page.data[key] = request.POST.get(key)
        ## update video
        if request.POST.get("video_link1"):
            page.data["video_link1"] = request.POST.get("video_link1")
        ## check perks then update
        for i in range(1, len(consultation_page_data["perks"]) + 1):
            title_key = f"perk.{i}.title"
            description_key = f"perk.{i}.description"
            image1_key = f"perk.{i}.image1"
            image2_key = f"perk.{i}.image2"

            if request.POST.get(title_key):
                page.data["perks"][i - 1]["title"] = request.POST.get(title_key)
            if request.POST.get(description_key):
                page.data["perks"][i - 1]["description"] = request.POST.get(
                    description_key
                )
            if request.FILES.get(image1_key):
                check_image_exists_then_delete(
                    page.data["perks"][i - 1]["image1"]["id"]
                )
                file = PageImage(page=page, image=request.FILES.get(image1_key))
                file.save()
                page.data["perks"][i - 1]["image1"] = {
                    "id": file.id,
                    "path": file.image.url,
                }
            if request.FILES.get(image2_key):
                check_image_exists_then_delete(
                    page.data["perks"][i - 1]["image2"]["id"]
                )
                file = PageImage(page=page, image=request.FILES.get(image2_key))
                file.save()
                page.data["perks"][i - 1]["image2"] = {
                    "id": file.id,
                    "path": file.image.url,
                }
        ## update consultation_reasons
        for i in range(1, len(consultation_page_data["consultation_reasons"]) + 1):
            title_key = f"reason.{i}.title"
            description_key = f"reason.{i}.description"
            image_key = f"reason.{i}.image"

            if request.POST.get(title_key):
                page.data["consultation_reasons"][i - 1]["title"] = request.POST.get(
                    title_key
                )
            if request.POST.get(description_key):
                page.data["consultation_reasons"][i - 1]["description"] = (
                    request.POST.get(description_key)
                )
            if request.FILES.get(image_key):
                check_image_exists_then_delete(
                    page.data["consultation_reasons"][i - 1]["image"]["id"]
                )
                file = PageImage(page=page, image=request.FILES.get(image_key))
                file.save()
                page.data["consultation_reasons"][i - 1]["image"] = {
                    "id": file.id,
                    "path": file.image.url,
                }
        page.save()

    return render(
        request,
        "pages/consultation.html",
        {"page": page.data},
    )


auth_page_data = {
    "bannerVideo": {
        "id": 1,
        "path": "bannerVideo/1.jpg",
    }
}
AUTH_PAGE = "auth"


def login_page(request):
    page = Page.objects.filter(page_name=AUTH_PAGE).first()

    if not page:
        page = Page(
            page_name=AUTH_PAGE,
            data=auth_page_data,
        )
        page.save()
    if request.method == "POST":
        ## Check header then update
        if request.FILES.get("bannerVideo"):
            check_image_exists_then_delete(page.data["bannerVideo"]["id"])
            file = PageVideo(page=page, video=request.FILES.get("bannerVideo"))
            file.save()
            page.data["bannerVideo"] = {
                "id": file.id,
                "path": file.video.url,
            }
        page.save()

    return render(
        request,
        "pages/auth.html",
        {"page": page.data},
    )
