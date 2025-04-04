from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import os
from products.models import (
    FAQ,
    ProductCategory,
    ProductSubCategory,
    ProductDesign,
    ProductSize,
    Product,
    ProductVariant,
    ProductDesignAssociation,
    ProductImage,
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from logging import getLogger

logger = getLogger(__name__)


def product_category_create_or_update(request, pk=None):
    product_category = None
    if pk:
        product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        descriptions = request.POST.get("descriptions")
        image = request.FILES.get("image")
        logger.info(request.FILES)

        if not category_name:
            messages.error(request, "Category name is required.")
            return redirect("product_category_create")

        if product_category:
            product_category.category_name = category_name
            product_category.descriptions = descriptions
            if image:
                product_category.image = image
            product_category.save()
            messages.success(request, "Product Category updated successfully!")
        else:
            ProductCategory.objects.create(
                category_name=category_name,
                descriptions=descriptions,
                image=image if image else None,
            )
            messages.success(request, "Product Category created successfully!")
        return redirect("product_category_list")
    return render(
        request,
        "product/category/product_category_form.html",
        {"product_category": product_category},
    )


def product_category_list(request):
    product_categories = ProductCategory.objects.all()
    return render(
        request,
        "product/category/product_category_list.html",
        {"product_categories": product_categories},
    )


def product_category_delete(request, pk):
    try:
        product_category = ProductCategory.objects.get(pk=pk)
        if product_category.image:
            if os.path.isfile(product_category.image.path):
                os.remove(product_category.image.path)
        product_category.delete()
        messages.success(request, "Product category deleted successfully!")
    except ProductCategory.DoesNotExist:
        messages.error(request, "The product category does not exist.")
    return redirect("product_category_list")


def product_subcategory_create_or_update(request, pk=None):
    product_subcategory = None
    product_categories = ProductCategory.objects.all().order_by("-created_at")

    if pk:
        product_subcategory = get_object_or_404(ProductSubCategory, pk=pk)

    if request.method == "POST":
        category_id = request.POST.get("category_id")
        subcategory_name = request.POST.get("subcategory_name")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not subcategory_name:
            messages.error(request, "Subcategory name is required.")
            return redirect("product_subcategory_create")

        product_category = get_object_or_404(ProductCategory, id=category_id)

        if product_subcategory:
            product_subcategory.subcategory_name = subcategory_name
            product_subcategory.description = description
            product_subcategory.category = product_category
            if image:
                product_subcategory.image = image
            product_subcategory.save()
            messages.success(request, "Product SubCategory updated successfully!")
        else:
            ProductSubCategory.objects.create(
                subcategory_name=subcategory_name,
                image=image,
                description=description,
                category=product_category,
            )
            messages.success(request, "Product SubCategory created successfully!")
        return redirect("product_subcategory_list")

    return render(
        request,
        "product/subcategory/product_subcategory_form.html",
        {
            "product_subcategory": product_subcategory,
            "product_categories": product_categories,
        },
    )


def product_subcategory_list(request):
    product_subcategories = ProductSubCategory.objects.all()
    return render(
        request,
        "product/subcategory/product_subcategory_list.html",
        {"product_subcategories": product_subcategories},
    )


def product_subcategory_delete(request, pk):
    try:
        product_subcategory = ProductSubCategory.objects.get(pk=pk)
        if product_subcategory.image:
            if os.path.isfile(product_subcategory.image.path):
                os.remove(product_subcategory.image.path)
        product_subcategory.delete()
        messages.success(request, "Product subcategory deleted successfully!")
    except ProductSubCategory.DoesNotExist:
        messages.error(request, "The product subcategory does not exist.")
    return redirect("product_subcategory_list")


def handle_image_update(instance, new_image, field_name):
    """Helper function to handle image updates"""
    if new_image:
        old_image = getattr(instance, field_name)
        if old_image and old_image.name:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
        setattr(instance, field_name, new_image)


def product_designs_create_or_update(request, pk=None):
    product_design = None
    if pk:
        product_design = get_object_or_404(ProductDesign, pk=pk)

    if request.method == "POST":
        if not request.POST.get("design_name"):
            messages.error(request, "Design name is required.")
            return redirect("product_designs_create")

        try:
            price = int(request.POST.get("design_price", 0))
        except ValueError:
            messages.error(request, "Invalid price value.")
            return redirect("product_designs_create")

        if product_design:
            product_design.design_name = request.POST.get("design_name")
            product_design.design_description = request.POST.get("design_description")
            product_design.design_price = price

            if "design_icon" in request.FILES:
                product_design.design_icon = request.FILES["design_icon"]

            for i in range(1, 4):
                image_field = f"design_image{i}"
                if image_field in request.FILES:
                    setattr(product_design, image_field, request.FILES[image_field])

            product_design.save()
            messages.success(request, "Product Design updated successfully!")
        else:
            design_data = {
                "design_name": request.POST.get("design_name"),
                "design_description": request.POST.get("design_description"),
                "design_price": price,
                "design_icon": request.FILES.get("design_icon"),
                "design_image": request.FILES.get("design_image"),
            }

            ProductDesign.objects.create(**design_data)
            messages.success(request, "Product Design created successfully!")

        return redirect("product_designs_list")

    context = {"product_designs": product_design}
    return render(request, "product/design/product_design_form.html", context)


def product_designs_list(request):
    designs = ProductDesign.objects.all()
    return render(
        request,
        "product/design/product_designs_list.html",
        {"product_designs": designs},
    )


def product_designs_delete(request, pk):
    try:
        product_design = ProductDesign.objects.get(pk=pk)

        image_fields = ["design_image", "design_icon"]
        for field in image_fields:
            image = getattr(product_design, field)
            if image and os.path.isfile(image.path):
                os.remove(image.path)

        product_design.delete()
        messages.success(request, "Product design deleted successfully!")

    except ProductDesign.DoesNotExist:
        messages.error(request, "The product design does not exist.")

    return redirect("product_designs_list")


def product_size_create_or_update(request, pk=None):
    product_size = None
    if pk:
        product_size = get_object_or_404(ProductSize, pk=pk)

    if request.method == "POST":
        size_name = request.POST.get("size_name")

        if not size_name:
            messages.error(request, "Size name is required.")
            return redirect("product_size_create")

        if product_size:
            product_size.size_name = size_name
            product_size.save()
            messages.success(request, "Product Size updated successfully!")
        else:
            ProductSize.objects.create(size_name=size_name)
            messages.success(request, "Product Size created successfully!")
        return redirect("product_size_list")

    return render(
        request, "product/size/product_size_form.html", {"product_size": product_size}
    )


def product_size_list(request):
    product_sizes = ProductSize.objects.all()
    return render(
        request, "product/size/product_size_list.html", {"product_sizes": product_sizes}
    )


def product_size_delete(request, pk):
    product_size = get_object_or_404(ProductSize, pk=pk)
    product_size.delete()
    messages.success(request, "Product size deleted successfully!")
    return redirect("product_size_list")


def product_create_or_update(request, pk=None):
    product = None
    categories = ProductCategory.objects.all()
    designs = ProductDesign.objects.all()

    if pk:
        product = get_object_or_404(Product, pk=pk)

    selected_design_ids = []
    if product:
        selected_design_ids = list(
            product.design_associations.values_list("design_id", flat=True)
        )

    if request.method == "POST":
        try:
            product_name = request.POST.get("product_name")
            category_id = request.POST.get("product_category")
            subcategory_id = request.POST.get("product_subcategory")
            selected_design_ids = request.POST.getlist("product_designs")
            beej_mantra = request.POST.get("beej_mantra")
            description = request.POST.get("description")

            if not product_name or not category_id:
                messages.error(request, "Product name and category are required.")
                return redirect(request.path)

            category = ProductCategory.objects.get(id=category_id)
            print(subcategory_id)
            subcategory = (
                ProductSubCategory.objects.get(id=subcategory_id)
                if subcategory_id
                else None
            )

            if product:
                product.product_name = product_name
                product.product_category = category
                product.product_subcategory = subcategory
                product.description = description
                product.beej_mantra = beej_mantra
                product.save()
            else:
                product = Product.objects.create(
                    product_name=product_name,
                    product_category=category,
                    product_subcategory=subcategory,
                    description=description,
                    beej_mantra=beej_mantra,
                )

            valid_design_ids = set(ProductDesign.objects.values_list("id", flat=True))

            selected_design_ids = [int(design_id) for design_id in selected_design_ids]

            if not set(selected_design_ids).issubset(valid_design_ids):
                messages.error(request, "Invalid design selection.")
                return redirect(request.path)

            product.design_associations.all().delete()
            for design_id in selected_design_ids:
                design = ProductDesign.objects.get(id=design_id)
                ProductDesignAssociation.objects.create(product=product, design=design)

            images = request.FILES.getlist("product_images")
            if images:
                product.images.all().delete()
                for image in images:
                    if image.size > 2 * 1024 * 1024:
                        messages.error(request, "Image size cannot exceed 2MB.")
                        continue
                    if not image.content_type.startswith("image/"):
                        messages.error(request, "Invalid image format.")
                        continue
                    ProductImage.objects.create(product=product, image=image)

            messages.success(
                request, f'Product {"updated" if pk else "created"} successfully!'
            )
            return redirect("product_list")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect(request.path)

    context = {
        "product": product,
        "categories": categories,
        "designs": designs,
        "selected_design_ids": selected_design_ids,
        "product_images": product.images.all() if product else [],
    }
    return render(request, "product/products/product_form.html", context)


def product_list(request):
    products = (
        Product.objects.select_related("product_category", "product_subcategory")
        .prefetch_related("variants", "design_associations", "images")
        .all()
    )
    return render(request, "product/products/product_list.html", {"products": products})


def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        for image in product.images.all():
            print("it is getting it")
            if image.image and os.path.isfile(image.image.path):
                print("it is getting it here too")
                os.remove(image.image.path)
        product.delete()
        messages.success(request, "Products deleted successfully!")
    except Product.DoesNotExist:
        messages.error(request, "The products does not exist.")
    return redirect("product_list")


def get_subcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = ProductSubCategory.objects.filter(category_id=category_id).values(
        "id", "subcategory_name"
    )
    return JsonResponse(list(subcategories), safe=False)


def product_image_create_or_update(request, pk=None):
    product_image = None
    products = Product.objects.all()

    if pk:
        try:
            product_image = ProductImage.objects.get(pk=pk)
        except ProductImage.DoesNotExist:
            messages.error(request, "The product image does not exist.")
            return redirect("product_image_list")

    if request.method == "POST":
        product_id = request.POST.get("product")
        image = request.FILES.get("image")

        if not product_id:
            messages.error(request, "Product selection is required.")
            return redirect("product_image_create")

        try:
            product = Product.objects.get(id=product_id)

            if product_image:

                if image:
                    if product_image.image:

                        if os.path.isfile(product_image.image.path):
                            os.remove(product_image.image.path)
                    product_image.image = image
                product_image.product = product
                product_image.save()
                messages.success(request, "Product image updated successfully!")
            else:

                if not image:
                    messages.error(request, "Image file is required.")
                    return redirect("product_image_create")

                ProductImage.objects.create(product=product, image=image)
                messages.success(request, "Product image created successfully!")

            return redirect("product_image_list")

        except Product.DoesNotExist:
            messages.error(request, "Selected product does not exist.")
            return redirect("product_image_create")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("product_image_create")

    context = {
        "product_image": product_image,
        "products": products,
    }
    return render(request, "product/image/product_image_form.html", context)


def product_image_list(request):
    product_images = ProductImage.objects.select_related("product").all()
    return render(
        request,
        "product/image/product_image_list.html",
        {"product_images": product_images},
    )


def product_image_delete(request, pk):
    try:
        product_image = ProductImage.objects.get(pk=pk)
        if product_image.image:
            if os.path.isfile(product_image.image.path):
                os.remove(product_image.image.path)
        product_image.delete()
        messages.success(request, "Product image deleted successfully!")
    except ProductImage.DoesNotExist:
        messages.error(request, "The product image does not exist.")
    return redirect("product_image_list")


def product_variant_create_or_update(request, pk=None):
    product_variant = None
    if pk:
        product_variant = get_object_or_404(ProductVariant, pk=pk)

    products = Product.objects.all()
    sizes = ProductSize.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        size_id = request.POST.get("size", None)
        price = request.POST.get("price", 0)
        stock = request.POST.get("stock", 0)

        if not product_id:
            messages.error(request, "Product is required.")
            return redirect("product_variant_create")

        try:
            price = int(price)
            stock = int(stock)
        except ValueError:
            messages.error(request, "Invalid price or stock value.")
            return redirect("product_variant_create")

        product = get_object_or_404(Product, id=product_id)

        size = ProductSize.objects.filter(id=size_id).first()

        if product_variant:
            product_variant.product = product
            product_variant.size = size
            product_variant.price = price
            product_variant.stock = stock
            product_variant.save()
            messages.success(request, "Product Variant updated successfully!")
        else:
            ProductVariant.objects.create(
                product=product, size=size, price=price, stock=stock
            )

            messages.success(request, "Product Variant created successfully!")
        return redirect("product_variant_list")

    context = {"product_variant": product_variant, "products": products, "sizes": sizes}
    return render(
        request, "product/product_variants/product_variant_form.html", context
    )


def product_variant_list(request):
    variants = ProductVariant.objects.select_related("product", "size").all()
    return render(
        request,
        "product/product_variants/product_variant_list.html",
        {"product_variants": variants},
    )


def product_variant_delete(request, pk):
    variant = get_object_or_404(ProductVariant, pk=pk)
    variant.delete()
    messages.success(request, "Product variant deleted successfully!")
    return redirect("product_variant_list")


def faq_create_or_update(request, pk=None):
    faq = None
    if pk:
        faq = get_object_or_404(FAQ, pk=pk)

    if request.method == "POST":
        question = request.POST.get("question")
        image = request.FILES.get("image", None)
        answer = request.POST.get("answer")
        category_id = request.POST.get("category")

        if not all([question, answer, category_id]):
            messages.error(request, "All fields are required.")
            return redirect("faq_create")

        category = get_object_or_404(ProductCategory, pk=category_id)

        # If an image is uploaded, remove any existing image for this category
        if image:
            existing_faq_with_image = (
                FAQ.objects.filter(category=category, image__isnull=False)
                .exclude(pk=pk)
                .first()
            )
            if existing_faq_with_image:
                existing_faq_with_image.image.delete()  # Delete old image
                existing_faq_with_image.image = None
                existing_faq_with_image.save()

        if faq:
            faq.question = question
            faq.answer = answer
            faq.category = category
            if image:
                faq.image = image  # Update image
            faq.save()
            messages.success(request, "FAQ updated successfully!")
        else:
            FAQ.objects.create(
                question=question, answer=answer, category=category, image=image
            )
            messages.success(request, "FAQ created successfully!")

        return redirect("faq_list")

    categories = ProductCategory.objects.all()
    return render(
        request, "product/faq/faq_form.html", {"faq": faq, "categories": categories}
    )


def faq_list(request):
    categories = ProductCategory.objects.prefetch_related("faq_items").all()
    return render(request, "product/faq/faq_list.html", {"categories": categories})


def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, "FAQ deleted successfully!")
    return redirect("faq_list")
