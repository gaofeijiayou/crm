class Pagination(object):

    def __init__(self, re,  count, per_page=10, max_show=10):
        current_page = re.GET.get('page', 0)

        import copy
        par = copy.deepcopy(re.GET)

        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page<=0:
            current_page = 1
        #每页显示多少数据

        #根据当前的页码获取到当前页显示的数据开始索引
        self.start_index = (current_page-1)*per_page
        #根据当前的页码获取到当前页显示的数据结束索引
        self.end_index = current_page*per_page
        #总共有多少数据

        #在一个页面中最多显示的页码数比如1 2 3 4 5 .....

        #计算出总共有多少页
        self.max_ye, m = divmod(count, per_page)
        if m:
            self.max_ye = self.max_ye+1

        if self.max_ye < max_show:
            max_show = self.max_ye

        #计算出当前页左边显示页码和右边显示的页码 比如8 9 10 11 12 13 1
        half_page = max_show // 2

        page_start = current_page - half_page
        page_end = current_page + half_page

        if page_start <= 1:
            page_start = 1
            page_end = max_show
        if page_end >= self.max_ye:
            page_end = self.max_ye
            page_start = self.max_ye - max_show + 1

        self.count_list = []
        par['page'] = current_page-1
        self.cur_p = '?{}'.format(par.urlencode())
        par['page'] = current_page+1
        self.cur_n = '?{}'.format(par.urlencode())
        par['page'] = 1
        self.first = '?{}'.format(par.urlencode())
        par['page'] = self.max_ye
        self.last = '?{}'.format(par.urlencode())
        for i in range(page_start, page_end+1):
            temp = {}
            par['page'] = i
            temp['url'] = '?{}'.format(par.urlencode())
            temp['val'] = i

            self.count_list.append(temp)



