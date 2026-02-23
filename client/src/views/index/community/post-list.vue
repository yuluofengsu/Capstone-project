<template>
  <div class="community-post-list">
    <Header />
    <div class="content-box">
      <div class="content-header">
        <h2>社区交流</h2>
        <div class="actions">
          <a-button type="primary" @click="$router.push('/index/community/post/create')">发布帖子</a-button>
          <a-button style="margin-left: 10px;" @click="$router.push('/index/community/event/list')">读书会活动</a-button>
        </div>
      </div>
      
      <div class="post-list">
        <div v-if="!loading && posts.length === 0" style="text-align: center; padding: 50px; color: #999;">
          暂无帖子，快来发布第一篇吧！
        </div>
        <a-list item-layout="vertical" size="large" :data-source="posts" :loading="loading">
          <a-list-item slot="renderItem" slot-scope="item, index" key="item.id" @click="goDetail(item.id)" class="post-item">
            <template slot="actions">
              <span>
                <a-icon type="eye" style="margin-right: 8px" />
                {{ item.views }}
              </span>
              <span>
                <a-icon type="like-o" style="margin-right: 8px" />
                {{ item.like_count }}
              </span>
              <span>
                <a-icon type="clock-circle" style="margin-right: 8px" />
                {{ item.create_time }}
              </span>
            </template>
            <a-list-item-meta :description="item.content.substring(0, 100) + '...'">
              <a slot="title" :href="'javascript:;'">{{ item.title }}</a>
              <a-avatar slot="avatar" :src="item.avatar || require('@/assets/images/avatar.jpg')" />
              <span slot="title" style="margin-left: 10px; font-size: 14px; color: #999;">{{ item.username }}</span>
            </a-list-item-meta>
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
import { listPost } from '@/api/index/community'

export default {
  components: {
    Header,
    Footer
  },
  data () {
    return {
      posts: [],
      loading: false
    }
  },
  mounted () {
    this.getPosts()
  },
  methods: {
    getPosts () {
      this.loading = true
      listPost().then(res => {
        this.loading = false
        if (res.code === 0) {
          this.posts = res.data
        } else {
          this.$message.error(res.msg)
        }
      }).catch(err => {
        this.loading = false
        console.error(err)
      })
    },
    goDetail (id) {
      this.$router.push({ name: 'postDetail', query: { id: id } })
    }
  }
}
</script>

<style scoped lang="less">
.community-post-list {
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
.post-item {
  cursor: pointer;
  &:hover {
    background: #fafafa;
  }
}
</style>
