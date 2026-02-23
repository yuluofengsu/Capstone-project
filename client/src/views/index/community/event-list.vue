<template>
  <div class="community-event-list">
    <Header />
    <div class="content-box">
      <div class="content-header">
        <h2>社区读书会活动</h2>
        <a-button @click="$router.push('/index/community/post/list')">返回社区</a-button>
      </div>
      
      <div class="event-list">
        <a-row :gutter="24">
          <a-col :span="8" v-for="item in events" :key="item.id" style="margin-bottom: 24px;">
            <a-card hoverable @click="goDetail(item.id)">
              <img slot="cover" :src="handleImageUrl(item.cover)" style="height: 200px; object-fit: cover;" />
              <a-card-meta :title="item.title">
                <template slot="description">
                  <div class="event-meta">
                    <p>{{ item.start_time }} 开始</p>
                    <p>状态: <span :class="'status-' + item.status">{{ getStatusText(item.status) }}</span></p>
                  </div>
                </template>
              </a-card-meta>
            </a-card>
          </a-col>
        </a-row>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
import { listEvent } from '@/api/index/community'
import { BASE_URL } from '@/store/constants'

export default {
  components: {
    Header,
    Footer
  },
  data () {
    return {
      events: [],
      loading: false
    }
  },
  mounted () {
    this.getEvents()
  },
  methods: {
    handleImageUrl (url) {
      if (!url) return ''
      if (url.startsWith('http')) return url
      return BASE_URL + url
    },
    getEvents () {
      this.loading = true
      listEvent().then(res => {
        this.loading = false
        if (res.code === 0) {
          this.events = res.data
        }
      })
    },
    goDetail (id) {
      this.$router.push({ name: 'eventDetail', query: { id: id } })
    },
    getStatusText (status) {
      const map = {
        '0': '未开始',
        '1': '进行中',
        '2': '已结束'
      }
      return map[status] || '未知'
    }
  }
}
</script>

<style scoped lang="less">
.community-event-list {
  background: #f6f6f6;
  min-height: 100vh;
  padding-top: 80px;
}
.content-box {
  width: 1000px;
  margin: 20px auto;
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  min-height: 600px;
}
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  
  h2 {
    font-size: 20px;
    font-weight: 600;
    color: #333;
  }
}
.status-0 { color: #1890ff; }
.status-1 { color: #52c41a; }
.status-2 { color: #999; }
</style>
