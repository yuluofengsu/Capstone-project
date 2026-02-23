<template>
  <div class="community-post-detail">
    <Header />
    <div class="content-box">
      <div class="post-detail" v-if="post">
        <div class="post-header">
          <h1>{{ post.title }}</h1>
          <div class="post-meta">
            <span>作者: {{ post.username }}</span>
            <span>发布时间: {{ post.create_time }}</span>
            <span>浏览: {{ post.views }}</span>
          </div>
        </div>
        <div class="post-content">
          {{ post.content }}
        </div>
        <div class="post-actions">
          <a-button :type="post.has_liked ? 'primary' : 'default'" icon="like" @click="handleLike">
            {{ post.has_liked ? '已点赞' : '点赞' }} ({{ post.like_count }})
          </a-button>
          <a-popconfirm
            title="确定要删除这篇帖子吗？"
            @confirm="handleDeletePost"
            okText="确定"
            cancelText="取消"
            v-if="isOwnerOrAdmin"
          >
            <a-button type="danger" icon="delete" style="margin-left: 10px;">删除</a-button>
          </a-popconfirm>
        </div>
      </div>
      
      <div class="comments-section">
        <h3>评论 ({{ comments.length }})</h3>
        <div class="comment-input">
          <a-textarea v-model="commentContent" :rows="3" placeholder="写下你的评论..." />
          <div style="text-align: right; margin-top: 10px;">
            <a-button type="primary" @click="submitComment">发表评论</a-button>
          </div>
        </div>
        
        <a-list class="comment-list" :header="`${comments.length} replies`" item-layout="horizontal" :data-source="comments">
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-comment :author="item.username" :avatar="handleImageUrl(item.avatar) || require('@/assets/images/avatar.jpg')">
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
import { detailPost, likePost, listComment, createComment, deleteComment, deletePost } from '@/api/index/community'
import { BASE_URL } from '@/store/constants'

export default {
  components: {
    Header,
    Footer
  },
  data () {
    return {
      post: null,
      comments: [],
      commentContent: '',
      id: this.$route.query.id
    }
  },
  computed: {
    isOwnerOrAdmin () {
      if (!this.post || !this.$store.state.user.userId) return false
      return this.post.user === this.$store.state.user.userId
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
      detailPost({ id: this.id }).then(res => {
        if (res.code === 0) {
          this.post = res.data
        }
      })
    },
    getComments () {
      listComment({ postId: this.id }).then(res => {
        if (res.code === 0) {
          this.comments = res.data
        }
      })
    },
    handleLike () {
      likePost({ id: this.id }).then(res => {
        if (res.code === 0) {
          if (this.post.has_liked) {
             this.post.like_count -= 1
             this.post.has_liked = false
             this.$message.success('取消点赞成功')
          } else {
             this.post.like_count += 1
             this.post.has_liked = true
             this.$message.success('点赞成功')
          }
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    handleDeletePost () {
      deletePost({ id: this.id }).then(res => {
        if (res.code === 0) {
          this.$message.success('删除成功')
          this.$router.push('/index/community/post/list')
        } else {
          this.$message.error(res.msg)
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
        post: this.id,
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
    handleDeleteComment (id) {
        deleteComment({ id: id }).then(res => {
            if (res.code === 0) {
                this.$message.success('删除成功')
                this.getComments()
            } else {
                this.$message.error(res.msg)
            }
        })
    }
  }
}
</script>

<style scoped lang="less">
.community-post-detail {
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
.post-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
  h1 {
    font-size: 24px;
    color: #333;
    margin-bottom: 10px;
  }
  .post-meta {
    color: #999;
    font-size: 14px;
    span {
      margin-right: 20px;
    }
  }
}
.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 30px;
  white-space: pre-wrap;
}
.post-actions {
  text-align: center;
  margin-bottom: 40px;
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
