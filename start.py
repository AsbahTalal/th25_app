import pygame as pg
import sys
import time


#obstacles code
obstacle_height = 200
obstacles = []
def create_obstacles():
    #bench
    bench_img = pg.image.load('bench.png',)
    ogWidth, ogHeight = bench_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    bench_img = pg.transform.scale((obstacle_height,obstacle_width))
    obstacles.append(bench_img)
    #duck
    duck_img = pg.image.load('duck.png',)
    ogWidth, ogHeight = duck_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    duck_img = pg.transform.scale(obstacle_height)
    obstacles.append(duck_img)
    #scooter
    scooter_img = pg.image.load('scooter.png',)
    ogWidth, ogHeight = scooter_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    scooter_img = pg.transform.scale(obstacle_height)
    obstacles.append(scooter_img)
    #person
    person1_img = pg.image.load('person1.png',)
    ogWidth, ogHeight = person1_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    person1_img = pg.transform.scale(obstacle_height)
    obstacles.append(person1_img)


obstacle_x = WIDTH #to be defined
obstacle_y = 0
obstacle_width = 0 #to be defined
obstacle_height = 0 #to be defined


