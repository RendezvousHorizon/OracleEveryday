from math import copysign, log10
import sqlite3
import cv2
import os
import numpy

image_dir = os.path.join(os.getcwd(), 'oracle-images')


def sql_query(query):
    conn = sqlite3.connect('OracleDB.db')
    cursor = conn.cursor()
    return cursor.execute(query)


def read_and_convert_to_binary(image_path):
    # load grayscale image
    im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # convert to binary image
    _, im = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)
    return 255 - im


def get_hu_moments(image_path):
    im = read_and_convert_to_binary(image_path)
    # calculate hu_moments and apply log transformation
    moments = cv2.moments(im)
    hu_moments = cv2.HuMoments(moments)
    for i in range(7):
        hu_moments[i] = -1 * copysign(1.0, hu_moments[i]) * log10(abs(hu_moments[i]))

    print(hu_moments)


def get_similarity(image1, image2):
    return cv2.matchShapes(image1, image2, cv2.CONTOURS_MATCH_I2, 0)


def get_top3(image_path):
    im0 = read_and_convert_to_binary(image_path)
    im0_name = sql_query('SELECT name FROM Oracle WHERE img="{}"'.format(os.path.basename(image_path))).fetchone()
    if im0_name is None:
        return None
    im0_name = im0_name[0][0]

    name_image_list = sql_query('SELECT name, img FROM Oracle').fetchall()

    cand_list = []
    threshold = 1e10
    cand = None
    for name, image_name in name_image_list:
        if name == im0_name:
            continue
        im = read_and_convert_to_binary(os.path.join(image_dir, image_name))
        score = get_similarity(im0, im)

        if len(cand_list) < 3:
            cand_list.append((name, score, image_name))
        elif threshold > score:
            cand_list[cand] = (name, score, image_name)
        threshold = max([c[1] for c in cand_list])
        for i in range(len(cand_list)):
            if cand_list[i][1] == threshold:
                cand = i
                break
    return cand_list


def create_questions():
    name_image_list = sql_query('SELECT name, img FROM Oracle').fetchall()
    questions = []
    count = 0
    prev_name = None
    for name, image_name in name_image_list:
        if name == prev_name:
            continue
        prev_name = name
        cand_list = get_top3(os.path.join(image_dir, image_name))
        if cand_list is not None:
            questions.append([image_name, name, cand_list[0][0], cand_list[1][0], cand_list[2][0]])
        count = count + 1
        if count > 30:
            break

    # save as sql file
    with open('flaskr/question.sql', 'w') as f:
        f.write('CREATE TABLE IF NOT EXISTS question (\n\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\n\
                img	TEXT,\n\
                a TEXT NOT NULL,\n\
                b TEXT NOT NULL,\n\
                c TEXT NOT NULL,\n\
                d TEXT NOT NULL,\n\
                FOREIGN KEY (img) REFERENCES oracle (img)\n\
            );\n')
        for q in questions:
            f.write('INSERT INTO question (img, a, b, c, d) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');\n'.format(q[0], q[1], q[2], q[3], q[4]))


if __name__ == '__main__':
    create_questions()
    pass




