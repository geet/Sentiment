from django.db import models

# Create your models here.

class data_set(models.Model):   
    tweet=models.CharField(max_length=200)
    tweet_hash = models.CharField(max_length=130,primary_key=True)	
    pos_neg=models.CharField(max_length=3)
    movie_name=models.CharField(max_length=50)
    def __unicode__(self):
        return (self.tweet,self.pos_neg,self.movie_name)


class pos_tokens(models.Model):
    ptoken = models.CharField(max_length=30)
    pcount = models.IntegerField()

    def __unicode__(self):
	return (self.id,self.token)

class neg_tokens(models.Model):
    ntoken = models.CharField(max_length=30)
    ncount = models.IntegerField()

    def __unicode__(self):
	return (self.id,self.token)

class tweet_category_count(models.Model):
    positive_count=models.IntegerField()
    negative_count=models.IntegerField()

class token_category_count(models.Model):
    positive_count=models.IntegerField()
    negative_count=models.IntegerField()
    
