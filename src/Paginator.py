class Paginator:
    def __init__(self, entries_limit):
        self.entries_limit = entries_limit
        self.p_entries = {}

    def insert(self, user, entries):
        self.user = user
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

    def page_next(self, user):
        self.p_entries[user]['curr_page_num'] += 1
        curr_page_num = self.p_entries[user]['curr_page_num']
        if curr_page_num not in self.p_entries[user]:
            self.p_entries[user]['curr_page_num'] -= 1
            curr_page_num -= 1
            #return []
        if curr_page_num not in self.p_entries[user]:
            return []
        return self.p_entries[user][curr_page_num]

    def page_prev(self, user):
        self.p_entries[user]['curr_page_num'] -= 1
        curr_page_num = self.p_entries[user]['curr_page_num']
        if curr_page_num not in self.p_entries[user]:
            self.p_entries[user]['curr_page_num'] += 1
            curr_page_num += 1
            #return self.p_entries[user][curr_page_num]
        if curr_page_num not in self.p_entries[user]:
            return []
        return self.p_entries[user][curr_page_num]

    def has_more_pages(self, user):
        if self.p_entries[user]['curr_page_num'] + 1 not in self.p_entries[user]:
            return False
        return True

    def has_prev_pages(self, user):
        if self.p_entries[user]['curr_page_num'] - 1 <= 0:
            return False
        return True


#user = 'evan'
#entries = ['a', 'b', 'c', 'd', 'e']
#p = Paginator(2)
#p.insert(user, entries)
#print p.page(user)
#print p.page(user)
#print p.page(user)
