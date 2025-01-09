from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BetAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bet_account')
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__ (self):
        return f'Username: {self.user.username}, {self.bonus} reais de bonus e {self.balance} reais no total'
    
    def deposit_bonus(self, amount):
        self.bonus += amount
        self.save()

    def wthdrawal_bonus(self, amount):
        if amount <= self.bonus:
            self.bonus -= amount
            self.save()
            return True
        else:
            return False
        
    def deposit_balance(self, amount):
        self.balance += amount
        self.save()

    def withdrawal_balance(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save()
            return True
        else:
            return False
    