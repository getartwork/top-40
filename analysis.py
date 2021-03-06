from pymongo import MongoClient
import numpy as np

def get_lyricless():
    client = MongoClient()
    db = client.top_40
    cursor = db.entries.find()
    for entry in cursor:
        if 'lyrics' not in entry:
            print entry['artist'].encode('utf-8') + ':' + entry['title'].encode('utf-8')
    cursor.close()

def get_yearcount():
    client = MongoClient()
    db = client.top_40
    i = 1950
    while i < 2016:
        cursor = db.entries.find({ "year": i, "lyrics": { "$exists": True }})
        full_cursor = db.entries.find({ "year": i })
        print str(i) + " , " + str(cursor.count()) + " / " + str(full_cursor.count())
        i += 1
    cursor.close()

def unique_word_count(lyrics):
    words = {}
    word_list = lyrics.split(" ")
    for word in word_list:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
    return len(words)

def song_length(lyrics):
    return len(lyrics.split(" "))

def word_len(lyrics):
    characters = 0;
    words = lyrics.split(" ")
    for word in words:
        characters += len(word)
    return characters * 1.0 / len(words)

def word_cv(lyrics):
    words = lyrics.split(" ")
    word_lens = []
    [word_lens.append(len(word)) for word in words]
    word_lens = np.array(word_lens)
    return np.std(word_lens) / word_len(lyrics)

def word_length_counts(lyrics):
    words = lyrics.split(" ")
    lengths = {}
    for word in words:
        word = word.replace("\'", '')
        if len(word) in lengths:
            lengths[len(word)] += 1
        else:
            lengths[len(word)] = 1

    for i in range(4,9):
        if not i in lengths:
            lengths[i] = 0

    return (
        lengths[4],
        lengths[5],
        lengths[6],
        lengths[7],
        lengths[8]
    )

def get_year_avg_word_count():
    client = MongoClient()
    db = client.top_40
    i = 1950
    print "Year, Average Unique Words Per Song, Average Song Length, Average Word Length Per Song, Word Length CV, Unique to Total Ratio, Unique Words CV, Four, Five, Six, Seven, Eight"
    while i < 2016:
        total_unique = 0
        total_len = 0
        total_avg_word = 0
        total_word_len_cv = 0
        total_unique_total_ratio = 0

        total_four = 0
        total_five = 0
        total_six = 0
        total_seven = 0
        total_eight = 0

        unique_words_per_song = []

        cursor = db.entries.find({ "year": i, "lyrics": { "$exists": True }})
        for entry in cursor:
            lyrics = entry['lyrics'].encode('utf-8')
            unique_words = unique_word_count(lyrics)
            unique_words_per_song.append(unique_words)

            song_len = song_length(lyrics)

            total_unique += unique_words
            total_len += song_len
            total_unique_total_ratio += unique_words * 1.0 / song_len
            total_avg_word += word_len(lyrics)
            total_word_len_cv += word_cv(lyrics)

            (four, five, six, seven, eight) = word_length_counts(lyrics)
            total_four += four
            total_five += five
            total_six += six
            total_seven += seven
            total_eight += eight

        avg_unique_words = total_unique * 1.0 / cursor.count()
        avg_song_len = total_len * 1.0 / cursor.count()
        avg_word_len = total_avg_word * 1.0 / cursor.count()
        avg_word_len_cv = total_word_len_cv * 1.0 / cursor.count()
        avg_unique_total_ratio = total_unique_total_ratio / cursor.count()
        avg_four = total_four * 1.0 / cursor.count()
        avg_five = total_five * 1.0 / cursor.count()
        avg_six = total_six * 1.0 / cursor.count()
        avg_seven = total_seven * 1.0 / cursor.count()
        avg_eight = total_eight * 1.0 / cursor.count()

        unique_words_cv = np.std(np.array(unique_words_per_song)) * 1.0 / avg_unique_words

        print str(i) + "," +\
            str(avg_unique_words) + "," +\
            str(avg_song_len) + "," +\
            str(avg_word_len) + "," +\
            str(avg_word_len_cv) + "," +\
            str(avg_unique_total_ratio) + "," +\
            str(unique_words_cv) + "," +\
            str(avg_four) + "," +\
            str(avg_five) + "," +\
            str(avg_six) + "," +\
            str(avg_seven) + "," +\
            str(avg_eight)
        i += 1

    cursor.close()

def get_year_word_count():
    client = MongoClient()
    db = client.top_40
    i = 1950
    while i < 2016:
        cursor = db.entries.find({ "year": i, "lyrics": { "$exists": True }})
        words = {}
        for entry in cursor:
            word_list = cursor['lyrics'].encode('utf-8').split(" ")
            for word in word_list:
                if words[word]:
                    words[word] += 1
                else:
                    words[word] = 1
        print str(i) + " , " + str(len(words))
        i += 1
    cursor.close()
