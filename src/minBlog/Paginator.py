
# TODO Don't store everything in memory/dict.
class Paginator:
    def __init__(self, entries_limit=0, comments_limit=0):
        self.entries_limit = entries_limit
        self.p_entries = {}
        self.comments_limit = comments_limit
        self.p_comments = {}

    def insert(self, entries, user=None):
        self.p_entries[user] = {}
        self.p_entries[user]['curr_page_num'] = 0
        count = 0
        curr_page_entries = []
        for entry in entries:
            if len(curr_page_entries) == self.entries_limit:
                self.p_entries[user][count + 1] = curr_page_entries
                curr_page_entries = []
                count += 1
            curr_page_entries.append(entry)
        if len(curr_page_entries) != 0:
            self.p_entries[user][count + 1] = curr_page_entries

    def page_next(self, user=None):
        self.p_entries[user]['curr_page_num'] += 1
        curr_page_num = self.p_entries[user]['curr_page_num']
        if curr_page_num not in self.p_entries[user]:
            self.p_entries[user]['curr_page_num'] -= 1
            curr_page_num -= 1
        if curr_page_num not in self.p_entries[user]:
            return []
        return self.p_entries[user][curr_page_num]

    def page_prev(self, user=None):
        self.p_entries[user]['curr_page_num'] -= 1
        curr_page_num = self.p_entries[user]['curr_page_num']
        if curr_page_num not in self.p_entries[user]:
            self.p_entries[user]['curr_page_num'] += 1
            curr_page_num += 1
        if curr_page_num not in self.p_entries[user]:
            return []
        return self.p_entries[user][curr_page_num]

    def has_more_pages(self, user=None):
        if self.p_entries[user]['curr_page_num'] + 1 not in self.p_entries[user]:
            return False
        return True

    def has_prev_pages(self, user=None):
        if self.p_entries[user]['curr_page_num'] - 1 <= 0:
            return False
        return True

    def populate_comments(self, comments, entry_id):
        self.p_comments[entry_id] = {}
        self.p_comments[entry_id]['all'] = comments
        page = 0
        self.p_comments[entry_id][page] = []
        for comment in comments:
            if len(self.p_comments[entry_id][page]) == self.comments_limit:
                page += 1
                self.p_comments[entry_id][page] = []
            self.p_comments[entry_id][page].append(comment)
        self.p_comments[entry_id]['curr_page_num'] = 0
        # print page
        self.p_comments[entry_id]['total_pages'] = page

    def get_comments(self, entry_id):
        if entry_id not in self.p_comments:
            return []
        return self.p_comments[entry_id]['all']

    def repopulate_comments(self, comment, entry_id):
        total_pages = self.p_comments[entry_id]['total_pages']
        curr_page_num = self.p_comments[entry_id]['curr_page_num']
        # new_page_num = curr_page_num
        # print new_page_num
        if total_pages in self.p_comments[entry_id] and \
                                len(self.p_comments[entry_id][total_pages]) + 1 > self.entries_limit:
            self.p_comments[entry_id]['total_pages'] += 1
            total_pages = self.p_comments[entry_id]['total_pages']
            self.p_comments[entry_id][total_pages] = []
        """elif new_page_num not in self.p_comments[entry_id]:
            self.p_comments[entry_id]['total_pages'] += 1
            self.p_comments[entry_id][new_page_num] = []"""
        # print total_pages
        self.p_comments[entry_id][total_pages].append(comment)
        # comments_so_far = []
        # print curr_page_num
        # for x in range(0, curr_page_num):
        #    for comment in self.p_comments[entry_id][x]:
        #        comments_so_far.append(comment)
        # print comments_so_far
        # return comments_so_far

    def load_more_comments(self, entry_id):
        curr_page_num = self.p_comments[entry_id]['curr_page_num']
        if curr_page_num > self.p_comments[entry_id]['total_pages']:
            return []
        # if len(self.p_comments[entry_id][curr_page_num]) == self.comments_limit:
        self.p_comments[entry_id]['curr_page_num'] += 1
        return self.p_comments[entry_id][curr_page_num]

    def has_more_comments(self, entry_id):
        curr_page_num = self.p_comments[entry_id]['curr_page_num']
        if curr_page_num > self.p_comments[entry_id]['total_pages']:
            return False
        return True

# user = 'evan'
# entries = ['a', 'b', 'c', 'd', 'e']
# p = Paginator(2)
# p.insert(user, entries)
# print p.page(user)
# print p.page(user)
# print p.page(user)
