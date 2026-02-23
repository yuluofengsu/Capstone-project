<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="活动标题" prop="title">
          <a-input placeholder="请输入" v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="封面">
          <a-upload-dragger
            name="file"
            accept="image/*"
            :multiple="false"
            :before-upload="beforeUpload"
          >
            <p class="ant-upload-drag-icon">
              <template v-if="coverUrl">
                <img :src="coverUrl"  style="width: 60px;height: 80px;"/>
              </template>
              <template v-else>
                <a-icon type="inbox" />
              </template>
            </p>
            <p class="ant-upload-text">
              请选择要上传的封面图片
            </p>
          </a-upload-dragger>
        </a-form-model-item>
      </a-col>

      <a-col span="24">
        <a-form-model-item label="活动介绍">
          <a-textarea placeholder="请输入" v-model="form.description" :rows="4"></a-textarea>
        </a-form-model-item>
      </a-col>
      
      <a-col span="12">
        <a-form-model-item label="开始时间" prop="start_time">
          <a-date-picker show-time placeholder="请选择" v-model="form.start_time" style="width: 100%;"/>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="结束时间" prop="end_time">
          <a-date-picker show-time placeholder="请选择" v-model="form.end_time" style="width: 100%;"/>
        </a-form-model-item>
      </a-col>

      <a-col span="12">
        <a-form-model-item label="状态">
          <a-select placeholder="请选择" allowClear v-model="form.status">
            <a-select-option key="0" value="0">未开始</a-select-option>
            <a-select-option key="1" value="1">进行中</a-select-option>
            <a-select-option key="2" value="2">已结束</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/event'

export default {
  name: 'EditEvent',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    event: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      coverUrl: undefined,
      form: {
        status: '0'
      },
      rules: {
        title: [{ required: true, message: '请输入活动标题', trigger: 'change' }],
        start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
        end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.event
      this.coverUrl = this.form.cover
      this.form.cover = undefined
      // moment objects for date picker if needed, but strings might work if format matches
      // Actually ant design vue date picker needs moment object or string depending on config
      // Assuming string works or will be handled
    }
  },
  methods: {
    beforeUpload (file) {
      const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
      const copyFile = new File([file], fileName)
      this.form.cover = copyFile
      return false
    },
    onOk () {
      return new Promise((resolve, reject) => {
        const formData = new FormData()
        formData.append('title', this.form.title)
        if (this.form.cover) {
          formData.append('cover', this.form.cover)
        }
        formData.append('description', this.form.description || '')
        
        if (this.form.start_time) {
          formData.append('start_time', this.$moment(this.form.start_time).format('YYYY-MM-DD HH:mm:ss'))
        }
        if (this.form.end_time) {
          formData.append('end_time', this.$moment(this.form.end_time).format('YYYY-MM-DD HH:mm:ss'))
        }
        if (this.form.status) {
          formData.append('status', this.form.status)
        }

        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              updateApi({
                id: this.event.id
              }, formData).then(res => {
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '更新失败')
                reject(new Error('更新失败'))
              })
            } else {
              createApi(formData).then(res => {
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '新建失败')
                reject(new Error('新建失败'))
              })
            }
          }
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
