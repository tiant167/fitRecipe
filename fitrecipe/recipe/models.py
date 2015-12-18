#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: chaihaotian
# @Date:   2015-04-26 14:30:44
# @Last Modified by:   chaihaotian
# @Last Modified time: 2015-07-25 17:22:57
from django.conf import settings
from django.db import models

from accounts.models import OtherAuthor
from base.models import BaseModel
from label.models import Label
from fitrecipe.utils import split_labels_into_list, str_to_int


class Recipe(BaseModel):
    '''
    recipe models
    '''
    # 菜谱id号(auto)，菜谱封面url，菜谱名称，功效，烹饪时间，卡路里，收藏数(redis)
    author = models.ForeignKey(OtherAuthor, null=True, blank=True) # 加上可空是为了迁移
    img = models.URLField(max_length=200, verbose_name=u'大图 URL')  # 图片全部使用 CDN
    thumbnail = models.URLField(max_length=200, verbose_name=u'缩略图 URL')
    recommend_img = models.URLField(max_length=200, null=True, blank=True, verbose_name=u'推荐大图 URL')
    recommend_thumbnail = models.URLField(max_length=200, null=True, blank=True, verbose_name=u'推荐缩略图 URL')
    title = models.CharField(max_length=100, verbose_name=u'菜谱名称')
    video = models.CharField(max_length=100, verbose_name=u'菜谱视频ID', default='', null=True)
    introduce = models.TextField(null=True, blank=True, verbose_name=u'菜谱简介')
    tips = models.TextField(null=True, blank=True, verbose_name=u'菜谱小贴士')
    duration = models.IntegerField(help_text=u'分钟', verbose_name=u'烹饪时间')  # 烹饪时间
    labels = models.ManyToManyField(Label, verbose_name=u'标签')
    calories = models.FloatField(default=0, verbose_name=u'每百克卡路里')
    collection_count = models.IntegerField(default=0, verbose_name=u'收藏数')
    status = models.IntegerField(default=-10, help_text=u'删除：-20，草稿: -10，正常：10', verbose_name=u'状态')
    procedures = models.TextField(default=u'[]', help_text=u'''JSON 字符串 <code>
        [{
          "content": "this is content",
          "img": "http://img.url"
        }]
    </code>''')
    components = models.TextField(default=u'[]', help_text=u'''JSON 字符串<code>
        [{
          "ingredient": "猪肉",
          "amount": 100,
          "remark": "this is remark tips"
        }]
    </code>''')
    water = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)
    carbohydrate = models.FloatField(default=0.0)
    fiber = models.FloatField(default=0.0)
    sodium = models.FloatField(default=0.0)
    vc = models.FloatField(default=0.0)
    vd = models.FloatField(default=0.0)
    fatty_acids = models.FloatField(default=0.0)
    cholesterol = models.FloatField(default=0.0)
    total_amount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = u'菜谱'
        verbose_name_plural = u'%s表' % verbose_name

    def __unicode__(self):
        return self.title

    def gcd(self, a, b):
        if a < b:
            a, b = b, a
        while b != 0:
            temp = a % b
            a = b
            b = temp
        return a

    def macro_element_ratio(self, list_format=False):
        ratio = (
            self.carbohydrate,
            self.protein,
            self.fat
            )
        if sum(ratio) == 0:
            ratio = [0, 0, 0]
        else:
            ratio = [int(v / sum(ratio) * 100) for v in ratio]
            first_gcd = self.gcd(ratio[0], ratio[1])
            second_gcd = self.gcd(ratio[1], ratio[2])
            third_gcd = self.gcd(first_gcd, second_gcd)
            ratio = [num/third_gcd for num in ratio]
        if list_format:
            return ratio
        else:
            return u'%d:%d:%d' % tuple(ratio)

    def protein_ratio(self):
        '''
        蛋白质在宏量元素比中占比
        '''
        ratio = self.macro_element_ratio(list_format=True)
        try:
            return u'%.2f%%' % (float(ratio[1])/ sum(ratio) * 100)
        except (ZeroDivisionError, TypeError):
            return u'0%'

    def fat_ratio(self):
        '''
        脂类在宏量元素比中占比
        '''
        ratio = self.macro_element_ratio(list_format=True)
        try:
            return u'%.2f%%' % (float(ratio[2])/ sum(ratio) * 100)
        except (ZeroDivisionError, TypeError):
            return u'0%'

    # django admin uses these attribute
    macro_element_ratio.short_description = u'宏量元素比'
    protein_ratio.short_description = u'蛋白质占比'
    fat_ratio.short_description = u'脂类占比'

    @classmethod
    def get_recipe_list(cls, labels, order, desc, start, num):
        '''
        根据条件获取菜谱列表

        labels: 4,5 (string) - label ID 使用逗号连接
        order: calories (string) - 排序方式，默认是 calories，其他可选值：duration（烹饪时间），收藏数（暂不支持）
        desc: false (string) - 是否倒序，默认是字符串 false，还可以是字符串 true
        start: 0 (string) - 偏移，默认是0。都是字符串，函数里会做转换，转成数字
        num: 10 (string) - 返回数量，默认是10。字符串
        '''
        recipes = cls.objects.all().filter(status__gt=0)
        # 逗号里面的是或 是并集 出现一个就好
        if labels is not None:
            # 对 食材 进行筛选
            recipes = recipes.filter(labels__id__in=split_labels_into_list(labels))
        if order == 'duration':
            recipes = recipes.order_by('duration')
        elif order == 'collection':
            recipes = recipes.order_by('collection_count')
        else:
            # 还有按照收藏数的排序，不过现在还没做
            # 默认按照卡路里
            recipes = recipes.order_by('calories')
        if desc == 'true':
            recipes = recipes.reverse()
        start = str_to_int(start, 0)
        num = str_to_int(num, 10)
        # bug in django 1.8.3, filter duplicate
        recipes = recipes.distinct()
        if num < 1:
            # 如果请求num数量小于 0 是不对的，改成 10
            num = 10
        if start < 0:
            # 如果 start 是负数，改成 0
            start = 0
        return recipes[start:num + start]

    @classmethod
    def get_latest_recipe(cls, start=0, num=10):
        return (cls.objects
            .select_related('author')
            .filter(status__gt=0)
            .order_by('-created_time')[start:start+num])


class Ingredient(BaseModel):
    name = models.CharField(max_length=25)
    eng_name = models.CharField(max_length=100, null=True, blank=True)  # 营养网站上的英文名名字，自动填入
    ndbno = models.CharField(max_length=25)  # 营养网站上的id, 要保留前面的0呐
    water = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carbohydrate = models.FloatField(null=True, blank=True)
    fiber = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    vc = models.FloatField(null=True, blank=True)
    vd = models.FloatField(null=True, blank=True)
    fatty_acids = models.FloatField(null=True, blank=True)
    cholesterol = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = '原料'
        verbose_name_plural = verbose_name + '表'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        捕捉save事件，通过英文名，去录入营养物质
        '''
        import requests
        import json
        # 先保存，不然后面外键指不到吧
        url = u'http://%s/usda/ndb/reports/?ndbno=%s&type=f&format=json&api_key=%s' % (settings.NDB_IP, self.ndbno, settings.NDB_API_KEY)
        resp = requests.get(url)
        if resp.status_code == 200:
            content = json.loads(resp.content)['report']['food']
            self.eng_name = content['name']
            # 保存完之后开始处理 nutritions
            nutri_dict = dict()
            for nu in content['nutrients']:
                # loop nutritions, 把他转成id做key的dict，不然查起来太费劲了
                nutri_dict[nu['nutrient_id']] = (nu['value'], nu['unit'])
            for item in settings.NDB_NUTRITION_ID_LIST:
                total = 0.0
                try:
                    if isinstance(item[0], tuple):
                        # 不饱和脂肪酸要求和
                        for sid in item[0]:
                            total += nutri_dict[sid][0]
                    else:
                        total = nutri_dict[item[0]][0]
                except KeyError:
                    # key 不存在
                    total = 0.0
                set_attr(self, item[1], total)
            return super(Ingredient, self).save(*args, **kwargs)
        elif resp.status_code == 400:
            raise AssertionError('400, check ndbno, dont forget the 0 before it')
        else:
            raise AssertionError('remote website said: %s' % resp.status_code)
