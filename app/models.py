from django.db import models


# Create your models here.

class CustomerAccount(models.Model):
    # 个人账户
    # 个人注册账户编号，位宽为10
    c_id = models.AutoField(primary_key=True)
    # 手机号码为主键
    c_phoneNo = models.IntegerField(max_length=18, unique=True)
    # 密码长度不能超过18位
    c_password = models.TextField(max_length=18)
    # 真实姓名
    c_truename = models.TextField(max_length=20)
    # 昵称
    c_nickname = models.TextField(max_length=20)
    # 性别,0代表女，1代表男
    c_gender = models.IntegerField(max_length=1)
    # 年龄
    c_age = models.IntegerField(max_length=10)
    # 电子邮箱地址
    c_email = models.TextField(max_length=64)
    # 住址信息
    c_addr = models.TextField(max_length=64)

    class Meta:
        db_table = 'CustomerAccount'


class MerchantAccount(models.Model):
    # 商家账户
    # 商家注册编号
    m_id = models.AutoField(primary_key=True)
    # 商家名称
    m_name = models.TextField(max_length=64)
    # 商家地址
    m_addr = models.TextField(max_length=64)
    # 商家注册日期
    m_registerdate = models.DateTimeField()
    # 商家联系电话
    m_phoneNo = models.IntegerField(max_length=18)
    # 商家信用分，基础分数500
    m_credit = models.IntegerField(max_length=3)
    # 商家的营业执照或认证证书
    m_certPic = models.ImageField(width_field=200, height_field=200)

    # 唯一性约束，商家的名称、地址和联系方式不能同时相同
    class Meta:
        unique_together = ('m_name', 'm_addr', 'm_phoneNo')
        db_table = 'MerchantAccount'


class ServiceForm(models.Model):
    # 针对每个商家的服务类型列表
    # 服务编号
    ms_signNo = models.AutoField(primary_key=True)
    # 外键，每个服务的集合对应一个商家id
    ms_id = models.ForeignKey(MerchantAccount, related_name='ms_id', on_delete=models.CASCADE, default='')
    # 服务类型，以编号的形式存储
    ms_type = models.IntegerField(max_length=10)
    # 服务详情
    ms_message = models.TextField(max_length=400)

    # 唯一性约束，同一个商家不可重复提交同一种服务
    class Meta:
        unique_together = ('ms_id', 'ms_type', 'ms_message')
        db_table = 'ServiceForm'


class OrderForm(models.Model):
    # 针对用户订单建立的服务记录表
    # 订单编号
    mo_signNo = models.AutoField(primary_key=True)
    # 订单上的用户id
    mo_oid = models.ForeignKey(CustomerAccount, related_name='mo_oid', on_delete=models.CASCADE, default='')
    # 订单上提供服务的商家id
    mo_sid = models.ForeignKey(MerchantAccount, related_name='mo_sid', on_delete=models.CASCADE, default='')
    # 服务类型
    mo_type = models.IntegerField(max_length=10)
    # 用户下了订单以后对订单的补充内容
    mo_message = models.TextField(max_length=140)

    # 用户提供的地址
    mo_addr = models.TextField(max_length=64)

    # 用户提供的联系方式
    mo_phoneNo = models.IntegerField(max_length=11)

    # 唯一性约束，同一个用户不能重复提交相同订单
    class Meta:
        unique_together = ('mo_oid', 'mo_sid', 'mo_phoneNo', 'mo_addr', 'mo_type', 'mo_message')
        db_table = 'OrderForm'
