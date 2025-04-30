from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор для моделей платежей."""
    class Meta:
        model = Payment
        fields = '__all__'


class UserCreateSerializer(ModelSerializer):
    """Сериализатор для создания моделей пользователей."""
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'city', 'profile_picture', 'password')


class UserUpdateSerializer(ModelSerializer):
    """Сериализатор для моделей пользователей, кроме создания."""
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'city', 'profile_picture')


class UserSerializer(ModelSerializer):
    """Сериализатор для моделей пользователей, кроме создания и редактирования."""
    # Добавляю поле платежи, чтобы выводилась история платежей пользователя
    payment_history = PaymentSerializer(many=True, source='user')

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'city', 'profile_picture', 'payment_history', 'password')


class UserNonCreatorSerializer(ModelSerializer):
    """Сериализатор для детального просмотра модели пользователя, если просматривающий пользователь не хозяин
    профиля."""
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'city', 'profile_picture')


class PaymentStatusSerializer(ModelSerializer):
    """Сериализатор для просмотра статуса платежа по id сессии"""
    class Meta:
        model = Payment
        fields = ('payment_status', 'id_session')