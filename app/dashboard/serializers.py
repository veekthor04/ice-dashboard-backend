from rest_framework import serializers

from core.models import Customer, Payment


class CustomerSerializer(serializers.ModelSerializer):
    """Customer Model Serializer"""

    balance = serializers.DecimalField(
        decimal_places=2, max_digits=18, read_only=True
    )

    class Meta:
        model = Customer
        exclude = ["id"]
        lookup_field = "customer_id"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    """Payment Model Serializer"""

    customer = CustomerSerializer()

    class Meta:
        model = Payment
        exclude = ["id"]
        lookup_field = "payment_ref"


class CreatePaymentSerializer(PaymentSerializer):
    """Payment Model Serializer to create using customer_id not id"""

    customer = serializers.SlugRelatedField(
        slug_field="customer_id", queryset=Customer.objects.all()
    )

    # setting $1 to be min transfer and required
    amount = serializers.DecimalField(
        required=True, decimal_places=2, max_digits=18, min_value=1.00
    )

    def create(self, validated_data):
        return super().create(validated_data)
