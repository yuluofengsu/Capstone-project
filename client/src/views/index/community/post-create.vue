<template>
  <div class="community-post-create">
    <Header />
    <div class="content-box">
      <div class="content-header">
        <h2>发布帖子</h2>
        <a-button @click="$router.go(-1)">返回</a-button>
      </div>
      
      <a-form :form="form" @submit="handleSubmit" style="margin-top: 20px;">
        <a-form-item label="标题" :label-col="{ span: 2 }" :wrapper-col="{ span: 20 }">
          <a-input v-decorator="['title', { rules: [{ required: true, message: '请输入标题' }] }]" placeholder="请输入标题" />
        </a-form-item>
        <a-form-item label="内容" :label-col="{ span: 2 }" :wrapper-col="{ span: 20 }">
          <a-textarea v-decorator="['content', { rules: [{ required: true, message: '请输入内容' }] }]" :rows="10" placeholder="请输入内容" />
        </a-form-item>
        <a-form-item :wrapper-col="{ span: 20, offset: 2 }">
          <a-button type="primary" html-type="submit" :loading="loading">发布</a-button>
        </a-form-item>
      </a-form>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
import { createPost } from '@/api/index/community'

export default {
  components: {
    Header,
    Footer
  },
  data () {
    return {
      form: this.$form.createForm(this),
      loading: false
    }
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      if (!this.$store.state.user.userId) {
        this.$message.warning('请先登录')
        return
      }
      this.form.validateFields((err, values) => {
        if (!err) {
          this.loading = true
          // Add user_id from store if needed, but usually backend handles it from token
          // Assuming backend gets user from token
          values.user = this.$store.state.user.userId 
          
          createPost(values).then(res => {
            this.loading = false
            if (res.code === 0) {
              this.$message.success('发布成功')
              this.$router.push('/index/community/post/list')
            } else {
              this.$message.error(res.msg)
            }
          }).catch(err => {
            this.loading = false
            console.error(err)
            this.$message.error('发布失败')
          })
        }
      })
    }
  }
}
</script>

<style scoped lang="less">
.community-post-create {
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
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  
  h2 {
    font-size: 20px;
    font-weight: 600;
    color: #333;
  }
}
</style>
