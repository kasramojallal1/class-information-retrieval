def heap_sort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]


def get_tokens(file_dir, normal_verbs, normal_prefix, normal_suffix, normal_junk, normal_common, token_dic, file_number):
    f = open(file_dir, "r", encoding='utf-8')
    flag_sum = 0

    for x in f:

        newline = x.split()

        for i in range(len(newline)):
            if '\u200c' in newline[i]:
                arr = newline[i].split('\u200c')
                for j in range(len(arr)):
                    newline.append(arr[j])
            if '\u200b' in newline[i]:
                arr = newline[i].split('\u200b')
                for j in range(len(arr)):
                    newline.append(arr[j])

        for i in range(len(newline)):

            if '\u200c' in newline[i]:
                continue

            flag_fix = 0

            if flag_sum == 1:
                flag_sum = 0
                continue

            #prefix normalizer
            for j in range(len(normal_prefix)):
                if normal_prefix[j] == newline[i]:
                    flag_fix = 1
                    break

            if flag_fix == 1:
                continue

            #junk normalizer
            for j in range(len(normal_junk)):
                if normal_junk[j] == newline[i]:
                    flag_fix = 1
                    break

            if flag_fix == 1:
                continue


            #suffix normalizer
            for j in range(len(normal_suffix)):
                if normal_suffix[j] == newline[i]:
                    flag_fix = 1
                    break

            if flag_fix == 1:
                continue

            # common normalizer
            for j in range(len(normal_common)):
                if normal_common[j] == newline[i]:
                    flag_fix = 1
                    break

            if flag_fix == 1:
                continue

            #junk characters
            for j in range(len(normal_junk)):
                newline[i] = newline[i].replace(normal_junk[j], '')


            #arabic characters
            newline[i] = newline[i].replace('ك', 'ک')
            newline[i] = newline[i].replace('ئ', 'ی')
            newline[i] = newline[i].replace('ي', 'ی')
            newline[i] = newline[i].replace('ؤ', 'و')
            newline[i] = newline[i].replace('هٔ', 'ه')
            newline[i] = newline[i].replace('ة', 'ه')
            newline[i] = newline[i].replace('آ', 'ا')
            newline[i] = newline[i].replace('أ', 'ا')
            newline[i] = newline[i].replace('إ', 'ا')
            newline[i] = newline[i].replace('۰', '')
            newline[i] = newline[i].replace('۱', '')
            newline[i] = newline[i].replace('۲', '')
            newline[i] = newline[i].replace('۳', '')
            newline[i] = newline[i].replace('۴', '')
            newline[i] = newline[i].replace('۵', '')
            newline[i] = newline[i].replace('۶', '')
            newline[i] = newline[i].replace('۷', '')
            newline[i] = newline[i].replace('۸', '')
            newline[i] = newline[i].replace('۹', '')


            #numerical normalizer
            if newline[i].isnumeric():
                continue


            #handle problems with verbs and nouns
            for j in range(len(normal_verbs)):
                if normal_verbs[j] in newline[i]:
                    value = newline[i].rfind(normal_verbs[j]) + len(normal_verbs[j])
                    arr = []
                    arr = newline[i]
                    try:
                        if arr[value]:
                            newline[i] = normal_verbs[j]
                            break
                    except:
                        continue

            #sum normalizer
            if i < len(newline) - 1:
                if newline[i+1] == 'ها':
                    flag_sum = 1
                if newline[i + 1] == 'های':
                    flag_sum = 1

            #greatness normalizer
            if i < len(newline) - 1:
                if newline[i+1] == 'تر':
                    flag_sum = 1
                elif newline[i+1] == 'ترین':
                    flag_sum = 1


            try:
                if token_dic[newline[i]]:
                    docs = token_dic[newline[i]]
                    docs.append(file_number)
                    token_dic[newline[i]] = docs

            except:
                token_dic[newline[i]] = [file_number]

    return token_dic


def read_files(path, normal_verbs, prefix, suffix, junk, common):
    files = []
    token_dic = {}
    new_token_dic = {}
    number_of_docs = 0
    tf_dic = {}
    df_dic = {}
    tf_idf_dic = {}
    final_tfidf = {}
    champion_list = {}


    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
                number_of_docs += 1

    for i in range(len(files)):
        text = files[i]
        text = text.replace('./data\\', '')
        text = text.replace('.txt', '')
        token_dic = get_tokens(files[i], normal_verbs, prefix, suffix, junk, common, token_dic, int(text))

    # print(token_dic)

    for key in token_dic:
        tf_dic[key] = [0 for i in range(number_of_docs)]

    for key in token_dic:
        arr = token_dic[key]
        tf_arr = tf_dic[key]

        for i in range(len(arr)):
            tf_arr[arr[i] - 1] += 1

        tf_dic[key] = tf_arr

    # print(tf_dic)

    for key in tf_dic:
        champion_list[key] = []

    for key in tf_dic:
        arr_tf = tf_dic[key]

        for i in range(len(arr_tf)):
            if arr_tf[i] > 3:
                arr_champ = champion_list[key]
                arr_champ.append(i)
                champion_list[key] = arr_champ

    # print(champion_list)



    for key in token_dic:
        arr = token_dic[key]
        x = np.array(arr)
        y = np.unique(x)
        y = y.tolist()
        df_dic[key] = len(y)

    # print(df_dic)


    for key in token_dic:
        tf_idf_dic[key] = [0 for i in range(number_of_docs)]


    for key in tf_idf_dic:
        arr_tfidf = tf_idf_dic[key]
        arr_tf = tf_dic[key]
        df = df_dic[key]


        for i in range(len(arr_tfidf)):
            if arr_tf[i] > 0:
                arr_tfidf[i] = math.log(1 + arr_tf[i], 10) * math.log(number_of_docs / df, 10)
            else:
                arr_tfidf[i] = 0

        tf_idf_dic[key] = arr_tfidf

    # print(tf_idf_dic)


    vocab_count = 0
    for key in tf_idf_dic:
        vocab_count += 1

    for i in range(number_of_docs):
        final_tfidf[i + 1] = [0 for i in range(vocab_count)]


    for key in final_tfidf:
        arr_final_tfidf = final_tfidf[key]

        count = 0
        for key0 in tf_idf_dic:
            arr_tfidf0 = tf_idf_dic[key0]
            arr_final_tfidf[count] = arr_tfidf0[int(key) - 1]
            count += 1

        final_tfidf[key] = arr_final_tfidf

    # print(final_tfidf)



    # write to files
    for key in token_dic:
        arr = token_dic[key]
        x = np.array(arr)
        y = np.unique(x)
        y = y.tolist()
        token_dic[key] = y


    sorted_keys = sorted(token_dic)

    for i in range(len(sorted_keys)):
        docs = token_dic[sorted_keys[i]]
        new_token_dic[sorted_keys[i]] = docs


    f = open("inverted-index.txt", "w", encoding='utf-8')
    f.write('')
    f.close()

    f = open("inverted-index.txt", "a", encoding='utf-8')
    for key in new_token_dic:
        if key == '':
            continue
        f.write(key + '\n' + '@' + '\n')
        arr = new_token_dic[key]
        for i in range(len(arr)):
            f.write(str(arr[i]) + '\n')
        f.write('@' + '\n')



    f = open("tfidf-index.txt", "w")
    f.write('')
    f.close()

    f = open("tfidf-index.txt", "a")
    for key in final_tfidf:
        f.write(str(key) + '\n' + '@' + '\n')
        arr = final_tfidf[key]
        for i in range(len(arr)):
            f.write(str(arr[i]) + '\n')
        f.write('@' + '\n')



    f = open("df-index.txt", "w", encoding='utf-8')
    f.write('')
    f.close()

    f = open("df-index.txt", "a", encoding='utf-8')
    for key in df_dic:
        f.write(str(key) + '\n' + '@' + '\n')
        f.write(str(df_dic[key]) + '\n')
        f.write('@' + '\n')



    f = open("champion_list.txt", "w", encoding='utf-8')
    f.write('')
    f.close()

    f = open("champion_list.txt", "a", encoding='utf-8')
    for key in champion_list:
        if key == '':
            continue
        f.write(key + '\n' + '@' + '\n')
        arr = champion_list[key]
        for i in range(len(arr)):
            f.write(str(arr[i]) + '\n')
        f.write('@' + '\n')


def tokenize():

    verbs, prefix, suffix, junk, common = normalizer_loader()

    read_files(path_documents, verbs, prefix, suffix, junk, common)


def tokenize_collected_data():
    verbs, prefix, suffix, junk, common = normalizer_loader()

    get_doc_centers(path_collected_data_health, verbs, prefix, suffix, junk, common, 'health')
    get_doc_centers(path_collected_data_history, verbs, prefix, suffix, junk, common, 'history')
    get_doc_centers(path_collected_data_math, verbs, prefix, suffix, junk, common, 'math')
    get_doc_centers(path_collected_data_physics, verbs, prefix, suffix, junk, common, 'physics')
    get_doc_centers(path_collected_data_tech, verbs, prefix, suffix, junk, common, 'tech')


def normalizer_loader():
    # verb normalizer
    f = open(path_verbs, "r", encoding='utf-8')
    verbs = f.readline()
    verbs = verbs.split()

    # prefix normalizer
    f = open(path_prefix, "r", encoding='utf-8')
    prefix = f.readline()
    prefix = prefix.split()

    # suffix normalizer
    f = open(path_suffix, "r", encoding='utf-8')
    suffix = f.readline()
    suffix = suffix.split()

    # junk normalizer
    f = open(path_junk, "r", encoding='utf-8')
    junk = f.readline()
    junk = junk.split()

    # common normalizer
    f = open(path_common, "r", encoding='utf-8')
    common = f.readline()
    common = common.split()

    return verbs, prefix, suffix, junk, common


def start_up(path):
    f = open(path, "r", encoding='utf-8')

    index_dictionary = {}
    arr = []

    for x in f:
        arr.append(x)

    for i in range(len(arr)):
        arr[i] = arr[i].replace('\n', '')


    flag_count = 0
    index_name = ''
    for i in range(len(arr)):
        if arr[i] == '@':
            if flag_count == 0:
                flag_count = 1
                continue
            else:
                flag_count = 0
                continue
        else:
            if flag_count == 0:
                index_dictionary[arr[i]] = []
                index_name = arr[i]
            else:
                docs = index_dictionary[index_name]
                docs.append(arr[i])

    return index_dictionary


def multi_word(words, dictionary):
    new_words = []

    for i in range(len(words)):
        try:
            if dictionary[words[i]]:
                new_words.append(words[i])
        except:
            continue

    arr = []

    for i in range(len(new_words)):
        arr.append(dictionary[new_words[i]])

    files = []
    for r, d, f in os.walk(path_documents):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))

    for i in range(len(files)):
        files[i] = files[i].replace('./data\\', '')
        files[i] = files[i].replace('.txt', '')

    result = []
    counter = 0
    for i in range(len(files)):
        for j in range(len(arr)):
            if files[i] in arr[j]:
                counter += 1
        result.append(counter)
        counter = 0

    result_dic = {}

    for i in range(len(result)):
        if result[i] == 0:
            continue
        result_dic[files[i]] = result[i]

    result_dic = dict(sorted(result_dic.items(), key=lambda item: item[1]))

    result_arr = []
    for key in result_dic.keys():
        result_arr.append(key)

    result_arr.reverse()

    print('\nResult is:')
    print(result_arr)
    print('')


def normalize_query(plain_text):

    words = plain_text.split()

    for i in range(len(words)):
        if '\u200c' in words[i]:
            arr = words[i].split('\u200c')
            for j in range(len(arr)):
                words.append(arr[j])
        if '\u200b' in words[i]:
            arr = words[i].split('\u200b')
            for j in range(len(arr)):
                words.append(arr[j])

    new_words = []
    flag_sum = 0

    verbs, prefix, suffix, junk, common = normalizer_loader()

    for i in range(len(words)):

        if '\u200c' in words[i]:
            continue

        flag_fix = 0

        if flag_sum == 1:
            flag_sum = 0
            continue


        # prefix normalizer
        for j in range(len(prefix)):
            if prefix[j] == words[i]:
                flag_fix = 1
                break

        if flag_fix == 1:
            continue

        # junk normalizer
        for j in range(len(junk)):
            if junk[j] == words[i]:
                flag_fix = 1
                break

        if flag_fix == 1:
            continue

        # suffix normalizer
        for j in range(len(suffix)):
            if suffix[j] == words[i]:
                flag_fix = 1
                break

        if flag_fix == 1:
            continue

        # common normalizer
        for j in range(len(common)):
            if common[j] == words[i]:
                flag_fix = 1
                break

        if flag_fix == 1:
            continue

        if words[i] == 'ببببببببب':
            continue

        # junk characters
        for j in range(len(junk)):
            words[i] = words[i].replace(junk[j], '')


        #arabic characters
        words[i] = words[i].replace('ك', 'ک')
        words[i] = words[i].replace('ئ', 'ی')
        words[i] = words[i].replace('ي', 'ی')
        words[i] = words[i].replace('ؤ', 'و')
        words[i] = words[i].replace('هٔ', 'ه')
        words[i] = words[i].replace('ة', 'ه')
        words[i] = words[i].replace('آ', 'ا')
        words[i] = words[i].replace('أ', 'ا')
        words[i] = words[i].replace('إ', 'ا')
        words[i] = words[i].replace('۰', '')
        words[i] = words[i].replace('۱', '')
        words[i] = words[i].replace('۲', '')
        words[i] = words[i].replace('۳', '')
        words[i] = words[i].replace('۴', '')
        words[i] = words[i].replace('۵', '')
        words[i] = words[i].replace('۶', '')
        words[i] = words[i].replace('۷', '')
        words[i] = words[i].replace('۸', '')
        words[i] = words[i].replace('۹', '')

        # numerical normalizer
        if words[i].isnumeric():
            continue

        # handle problems with verbs and nouns
        for j in range(len(verbs)):
            if verbs[j] in words[i]:
                value = words[i].rfind(verbs[j]) + len(verbs[j])
                arr = []
                arr = words[i]
                try:
                    if arr[value]:
                        words[i] = verbs[j]
                        break
                except:
                    continue

        # sum normalizer
        if words[i] == 'ها':
            continue
        if words[i] == 'تر':
            continue
        if words[i] == 'ترین':
            continue

        new_words.append(words[i])

    print(new_words)

    return new_words


def answer_by_cosine(words, df_dic, tfidf_dic, k, if_champion):

    query_dic = {}
    tf_query_dic = {}
    number_of_docs = 0
    if_used = if_champion
    global path_documents

    for r, d, f in os.walk(path_documents):
        for file in f:
            if '.txt' in file:
                number_of_docs += 1

    for i in range(len(words)):
        try:
            if query_dic[words[i]]:
                num = query_dic[words[i]]
                num += 1
                query_dic[words[i]] = num

        except:
            query_dic[words[i]] = 1


    for key in df_dic:
        try:
            if query_dic[key]:
                tf_query_dic[key] = query_dic[key]
        except:
            tf_query_dic[key] = 0

    query_arr = []

    for key in tf_query_dic:

        tf = tf_query_dic[key]
        nt = df_dic[key]
        nt = int(nt[0])

        if tf > 0:
            query_arr.append(math.log(1 + tf, 10) * math.log(number_of_docs / nt, 10))

        else:
            query_arr.append(0)



    arr_cosine = []
    b = query_arr
    sum_b = 0
    for i in range(len(b)):
        sum_b += math.pow(b[i], 2)
    rad_b = math.sqrt(sum_b)

    for key in tfidf_dic:
        a = tfidf_dic[key]

        for i in range(len(a)):
            a[i] = float(a[i])

        sum_a = 0
        for i in range(len(a)):
            sum_a += math.pow(a[i], 2)
        rad_a = math.sqrt(sum_a)

        arr_cosine.append(np.dot(a, b) / rad_a * rad_b)


    similarity_dic = {}

    for i in range(len(arr_cosine)):
        similarity_dic[i + 1] = arr_cosine[i]

    # print('sim dic:')
    # print(similarity_dic)

    key_list = list(similarity_dic.keys())
    val_list = list(similarity_dic.values())

    result = heap_sort(arr_cosine)
    final_result = []
    f_result = []


    for value in reversed(result):
        if value > 0:
            final_result.append(key_list[val_list.index(value)])
        else:
            continue


    for i in range(len(final_result)):
        if i >= k:
            break
        f_result.append(final_result[i])

    print('\nResult is:')
    print(f_result)
    print('')


def answer_by_cosine_collected(words, df_dic, tfidf_dic, path):
    query_dic = {}
    tf_query_dic = {}
    number_of_docs = 0

    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                number_of_docs += 1

    for i in range(len(words)):
        try:
            if query_dic[words[i]]:
                num = query_dic[words[i]]
                num += 1
                query_dic[words[i]] = num

        except:
            query_dic[words[i]] = 1

    for key in df_dic:
        try:
            if query_dic[key]:
                tf_query_dic[key] = query_dic[key]
        except:
            tf_query_dic[key] = 0


    query_arr = []

    for key in tf_query_dic:

        tf = tf_query_dic[key]
        nt = df_dic[key]
        nt = int(nt[0])

        if tf > 0:
            query_arr.append(math.log(1 + tf, 10) * math.log(number_of_docs / nt, 10))

        else:
            query_arr.append(0)


    arr_cosine = []
    b = query_arr
    sum_b = 0
    for i in range(len(b)):
        sum_b += math.pow(b[i], 2)
    rad_b = math.sqrt(sum_b)

    for key in tfidf_dic:
        a = tfidf_dic[key]

        for i in range(len(a)):
            a[i] = float(a[i])

        sum_a = 0
        for i in range(len(a)):
            sum_a += math.pow(a[i], 2)
        rad_a = math.sqrt(sum_a)

        arr_cosine.append(np.dot(a, b) / rad_a * rad_b)

    return arr_cosine[0]


def get_doc_centers(path, normal_verbs, prefix, suffix, junk, common, doc_type):
    files = []
    token_dic = {}
    number_of_docs = 0
    tf_dic = {}
    df_dic = {}
    tf_idf_dic = {}
    final_tfidf = {}

    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
                number_of_docs += 1



    for i in range(len(files)):
        text = files[i]
        text = text.replace('./collected-data/' + doc_type + '\\', '')
        text = text.replace('.txt', '')
        text = text.replace(' ', '')
        text = text.replace('(', '')
        text = text.replace(')', '')
        token_dic = get_tokens(files[i], normal_verbs, prefix, suffix, junk, common, token_dic, int(text))


    for key in token_dic:
        tf_dic[key] = [0 for i in range(number_of_docs)]

    for key in token_dic:
        arr = token_dic[key]
        tf_arr = tf_dic[key]

        for i in range(len(arr)):
            tf_arr[arr[i] - 1] += 1

        tf_dic[key] = tf_arr



    for key in token_dic:
        arr = token_dic[key]
        x = np.array(arr)
        y = np.unique(x)
        y = y.tolist()
        df_dic[key] = len(y)


    for key in token_dic:
        tf_idf_dic[key] = [0 for i in range(number_of_docs)]


    for key in tf_idf_dic:
        arr_tfidf = tf_idf_dic[key]
        arr_tf = tf_dic[key]
        df = df_dic[key]


        for i in range(len(arr_tfidf)):
            if arr_tf[i] > 0:
                arr_tfidf[i] = math.log(1 + arr_tf[i], 10) * math.log(number_of_docs / df, 10)
            else:
                arr_tfidf[i] = 0

        tf_idf_dic[key] = arr_tfidf

    # print(tf_idf_dic)


    vocab_count = 0
    for key in tf_idf_dic:
        vocab_count += 1

    print(doc_type + ' : ' + str(vocab_count))

    for i in range(number_of_docs):
        final_tfidf[i + 1] = [0 for i in range(vocab_count)]


    for key in final_tfidf:
        arr_final_tfidf = final_tfidf[key]

        count = 0
        for key0 in tf_idf_dic:
            arr_tfidf0 = tf_idf_dic[key0]
            arr_final_tfidf[count] = arr_tfidf0[int(key) - 1]
            count += 1

        final_tfidf[key] = arr_final_tfidf

    # print(final_tfidf)


    center_vector = [[] for i in range(vocab_count)]

    for key in final_tfidf:

        arr_final_tfidf = final_tfidf[key]

        for i in range(len(arr_final_tfidf)):
            center_vector[i].append(arr_final_tfidf[i])

    for i in range(len(center_vector)):
        my_arr = center_vector[i]
        my_sum = sum(my_arr)

        my_avg = my_sum / len(my_arr)

        center_vector[i] = my_avg



    f = open("./wiki-vectors/center-" + doc_type + ".txt", "w")
    f.write('')
    f.close()

    f = open("./wiki-vectors/center-" + doc_type + ".txt", "a")
    for i in range(len(center_vector)):
        f.write(str(center_vector[i]) + '\n')




    f = open("./wiki-vectors/tfidf-index-" + doc_type + ".txt", "w")
    f.write('')
    f.close()

    f = open("./wiki-vectors/tfidf-index-" + doc_type + ".txt", "a")
    for key in final_tfidf:
        f.write(str(key) + '\n' + '@' + '\n')
        arr = final_tfidf[key]
        for i in range(len(arr)):
            f.write(str(arr[i]) + '\n')
        f.write('@' + '\n')



    f = open("./wiki-vectors/df-index-" + doc_type + ".txt", "w", encoding='utf-8')
    f.write('')
    f.close()

    f = open("./wiki-vectors/df-index-" + doc_type + ".txt", "w", encoding='utf-8')
    for key in df_dic:
        f.write(str(key) + '\n' + '@' + '\n')
        f.write(str(df_dic[key]) + '\n')
        f.write('@' + '\n')


def which_type(words):
    f_health = open('./wiki-vectors/center-health.txt', "r", encoding='utf-8')
    f_history = open('./wiki-vectors/center-history.txt', "r", encoding='utf-8')
    f_math = open('./wiki-vectors/center-math.txt', "r", encoding='utf-8')
    f_physics = open('./wiki-vectors/center-physics.txt', "r", encoding='utf-8')
    f_tech = open('./wiki-vectors/center-tech.txt', "r", encoding='utf-8')


    arr_health = []
    arr_history = []
    arr_math = []
    arr_physics = []
    arr_tech = []

    for x in f_health:
        arr_health.append(x)
    for x in f_history:
        arr_history.append(x)
    for x in f_math:
        arr_math.append(x)
    for x in f_physics:
        arr_physics.append(x)
    for x in f_tech:
        arr_tech.append(x)

    for i in range(len(arr_health)):
        arr_health[i] = arr_health[i].replace('\n', '')
    for i in range(len(arr_history)):
        arr_history[i] = arr_history[i].replace('\n', '')
    for i in range(len(arr_math)):
        arr_math[i] = arr_math[i].replace('\n', '')
    for i in range(len(arr_physics)):
        arr_physics[i] = arr_physics[i].replace('\n', '')
    for i in range(len(arr_tech)):
        arr_tech[i] = arr_tech[i].replace('\n', '')


    tfidf_health_dic = {1: arr_health}
    df_health_dic = start_up('./wiki-vectors/df-index-health.txt')

    cosine_health = answer_by_cosine_collected(words, df_health_dic, tfidf_health_dic, './collected-data/health')

    tfidf_history_dic = {1: arr_history}
    df_history_dic = start_up('./wiki-vectors/df-index-history.txt')

    cosine_history = answer_by_cosine_collected(words, df_history_dic, tfidf_history_dic, './collected-data/history')

    tfidf_math_dic = {1: arr_math}
    df_math_dic = start_up('./wiki-vectors/df-index-math.txt')

    cosine_math = answer_by_cosine_collected(words, df_math_dic, tfidf_math_dic, './collected-data/math')

    tfidf_physics_dic = {1: arr_physics}
    df_physics_dic = start_up('./wiki-vectors/df-index-physics.txt')

    cosine_physics = answer_by_cosine_collected(words, df_physics_dic, tfidf_physics_dic, './collected-data/physics')

    tfidf_tech_dic = {1: arr_tech}
    df_tech_dic = start_up('./wiki-vectors/df-index-tech.txt')

    cosine_tech = answer_by_cosine_collected(words, df_tech_dic, tfidf_tech_dic, './collected-data/tech')


    cosine_similarity_dic = {'health': cosine_health,
                             'history': cosine_history,
                             'math': cosine_math,
                             'physics': cosine_physics,
                             'tech': cosine_tech}

    # print(cosine_similarity_dic)

    all_values = cosine_similarity_dic.values()
    max_value = max(all_values)

    for key in cosine_similarity_dic:
        if cosine_similarity_dic[key] == max_value:
            return key


    return 'problem'


if __name__ == '__main__':
    import os
    import numpy as np
    import math
    import heapq


    path_documents = './data'
    path_verbs = './normalizer/verbs.txt'
    path_prefix = './normalizer/prefix.txt'
    path_suffix = './normalizer/suffix.txt'
    path_junk = './normalizer/junk.txt'
    path_common = './normalizer/common.txt'
    path_inverted_index = 'inverted-index.txt'
    path_tfidf_index = 'tfidf-index.txt'
    path_df_index = 'df-index.txt'
    path_collected_data_health = './collected-data/health'
    path_collected_data_math = './collected-data/math'
    path_collected_data_physics = './collected-data/physics'
    path_collected_data_history = './collected-data/history'
    path_collected_data_tech = './collected-data/tech'



    while True:
        query = ''
        choice = input('1. single word search   2. multi word search    3.tokenize'
                       '   4.test function   5.cosine    6.cosine with champion list'
                       '    7.get doc centers   8.search with doc type\n')

        if choice == '1':
            try:
                inverted_dic = start_up(path_inverted_index)
            except:
                print('tokenize first')
                continue

            query = input('Enter your query(single word): ')
            query = query + ' ببببببببب'
            query = normalize_query(query)
            try:
                print('\nResult is:')
                print(inverted_dic[query[0]])
                print('')
            except:
                print('no such word in any document\n')


        if choice == '2':
            try:
                inverted_dic = start_up(path_inverted_index)
            except:
                print('tokenize first')
                continue

            query = input('Enter your query: ')
            query = normalize_query(query)
            multi_word(query, inverted_dic)


        if choice == '3':
            tokenize()



        if choice == '4':
            try:
                inverted_dic = start_up(path_inverted_index)
            except:
                print('tokenize first')
                continue


            query = input('which word: ')
            query = query + ' ببببببببب'
            query = normalize_query(query)
            try:
                print(inverted_dic[query[0]])
            except:
                print('no such word in any document\n')


        if choice == '5':

            try:
                my_tfidf_dic = start_up(path_tfidf_index)
                my_df_dic = start_up(path_df_index)
            except:
                print('tokenize first')
                continue

            query = input('Enter your query: ')
            query = normalize_query(query)
            answer_by_cosine(query, my_df_dic, my_tfidf_dic, 5, 0)



        if choice == '6':

            try:
                my_tfidf_dic = start_up(path_tfidf_index)
                my_df_dic = start_up(path_df_index)
            except:
                print('tokenize first')
                continue

            query = input('Enter your query: ')
            query = normalize_query(query)
            answer_by_cosine(query, my_df_dic, my_tfidf_dic, 5, 1)


        if choice == '7':
            tokenize_collected_data()


        if choice == '8':

            query = input('Enter your query: ')
            query = normalize_query(query)

            type_id = which_type(query)
            print(type_id)

            if type_id != 'problem':
                try:
                    my_tfidf_dic = start_up('./wiki-vectors/tfidf-index-' + type_id + '.txt')
                    my_df_dic = start_up('./wiki-vectors/df-index-' + type_id + '.txt')
                except:
                    print('tokenize first')
                    continue

                answer_by_cosine(query, my_df_dic, my_tfidf_dic, 5, 1)

