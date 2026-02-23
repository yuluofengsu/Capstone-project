<template>
  <div class="community-event-detail">
    <Header />
    <div class="content-box">
      <div class="event-detail" v-if="event">
        <div class="event-header">
          <h1>{{ event.title }}</h1>
          <div class="event-meta">
            <p>时间: {{ event.start_time }} ~ {{ event.end_time }}</p>
            <p>状态: {{ getStatusText(event.status) }}</p>
          </div>
          <div class="event-cover" v-if="event.cover">
              <img :src="handleImageUrl(event.cover)" style="max-width: 100%; max-height: 400px;" />
          </div>
        </div>
        <div class="event-content">
          <h3>活动介绍</h3>
          <p>{{ event.description }}</p>
        </div>
      </div>
      
      <div class="comments-section">
        <h3>讨论区 ({{ comments.length }})</h3>
        <div class="comment-input">
          <a-textarea v-model="commentContent" :rows="3" placeholder="发表你的看法..." />
          <div style="text-align: right; margin-top: 10px;">
            <a-button type="primary" @click="submitComment">发表评论</a-button>
          </div>
        </div>
        
        <a-list class="comment-list" :header="`${comments.length} replies`" item-layout="horizontal" :data-source="comments">
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-comment :author="item.username" :avatar="item.avatar || require('@/assets/images/avatar.jpg')">
              <template slot="actions">
                <span v-if="item.user === $store.state.user.userId" @click="handleDeleteComment(item.id)">删除</span>
              </template>
              <p slot="content">{{ item.content }}</p>
              <a-tooltip slot="datetime" :title="item.create_time">
                <span>{{ item.create_time }}</span>
              </a-tooltip>
            </a-comment>
          </a-list-item>
        </a-list>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
import { detailEvent, listComment, createComment, deleteComment } from '@/api/index/community'
import { BASE_URL } from '@/store/constants'

export default {
  components: {
    Header,
    Footer
  },
  data () {
    return {
      event: null,
      comments: [],
      commentContent: '',
      id: this.$route.query.id
    }
  },
  mounted () {
    this.getDetail()
    this.getComments()
  },
  methods: {
    handleImageUrl (url) {
      if (!url) return ''
      if (url.startsWith('http')) return url
      return BASE_URL + url
    },
    getDetail () {
      detailEvent({ id: this.id }).then(res => {
        if (res.code === 0) {
          this.event = res.data
        }
      })
    },
    getComments () {
      listComment({ event_id: this.id }).then(res => {
        if (res.code === 0) {
          this.comments = res.data
        }
      })
    },
    submitComment () {
      if (!this.$store.state.user.userId) {
        this.$message.warning('请先登录')
        return
      }
      if (!this.commentContent) {
        this.$message.warning('请输入评论内容')
        return
      }
      createComment({
        event: this.id,
        content: this.commentContent,
        user: this.$store.state.user.userId
      }).then(res => {
        if (res.code === 0) {
          this.$message.success('评论成功')
          this.commentContent = ''
          this.getComments()
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    getStatusText (status) {
      const map = {
        '0': '未开始',
        '1': '进行中',
        '2': '已结束'
      }
      return map[status] || '未知'
    },
    handleDeleteComment (id) {
        deleteComment({ id: id }).then(res => {
            if (res.code === 0) {
                this.$message.success('删除成功')
                this.getComments()
            } else {
                this.$message.error(res.msg)
            }
        })
    },
    joinEvent () {
      if (!this.$store.state.user.userId) {
        this.$message.warning('请先登录')
        return
      }
      this.$message.success('报名成功')
    }
  }
}
</script>

<style scoped lang="less">
.community-event-detail {
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
.event-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
  h1 {
    font-size: 24px;
    color: #333;
    margin-bottom: 10px;
  }
  .event-meta {
    color: #666;
    font-size: 14px;
    margin-bottom: 20px;
  }
}
.event-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 30px;
  h3 {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 10px;
  }
}
.comments-section {
  border-top: 1px solid #eee;
  padding-top: 20px;
  h3 {
    margin-bottom: 20px;
  }
  .comment-input {
    margin-bottom: 30px;
  }
}
</style>
