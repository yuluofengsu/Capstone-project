<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
        <a-button type="primary" @click="handleAdd">新增</a-button>
        <a-button @click="handleBatchDelete">批量删除</a-button>
      </a-space>
    </div>
    <div class="table-wrap" ref="tableWrap">
      <a-table
        size="middle"
        rowKey="id"
        :loading="loading"
        :columns="columns"
        :data-source="data"
        :scroll="{ x: 'max-content' }"
        :row-selection="rowSelection()"
        :pagination="{
          size: 'default',
          current: page,
          pageSize: pageSize,
          onChange: (current) => page = current,
          pageSizeOptions: ['10', '20', '30', '40'],
          showSizeChanger: true,
          showTotal: (total) => `共${total}条数据`
        }"
      >
        <span slot="cover" slot-scope="text">
          <img :src="text" style="width: 40px;height: 60px;"/>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">编辑</a>
            <a @click="handleDelete(record)">删除</a>
          </a-space>
        </span>
      </a-table>
    </div>
  </div>
</template>

<script>
import {listApi, deleteApi} from '@/api/admin/event'
import EditEvent from '@/views/admin/model/edit-event'

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    width: 60
  },
  {
    title: '活动标题',
    dataIndex: 'title',
    key: 'title'
  },
  {
    title: '封面',
    dataIndex: 'cover',
    key: 'cover',
    scopedSlots: { customRender: 'cover' }
  },
  {
    title: '开始时间',
    dataIndex: 'start_time',
    key: 'start_time'
  },
  {
    title: '结束时间',
    dataIndex: 'end_time',
    key: 'end_time'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    customRender: (text) => {
      if (text === '0') return '未开始'
      if (text === '1') return '进行中'
      if (text === '2') return '已结束'
      return text
    }
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'Event',
  data () {
    return {
      loading: false,
      selectedRowKeys: [],
      columns,
      data: [],
      pageSize: 10,
      page: 1
    }
  },
  methods: {
    getList () {
      this.loading = true
      listApi().then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
          if (item.cover) {
            const coverString = String(item.cover);
            const decodedCover = decodeURIComponent(coverString);
            if (decodedCover.includes('http') || decodedCover.includes('https')) {
              if (decodedCover.startsWith('/upload/')) {
                item.cover = decodedCover.slice(8);
              } else {
                item.cover = decodedCover;
              }
            } else {
              item.cover = this.$BASE_URL + decodedCover;
            }
          }
        })
        this.data = res.data
      }).catch(err => {
        this.$message.error(err.msg)
        this.loading = false
      })
    },
    rowSelection () {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          this.selectedRowKeys = selectedRowKeys
        }
      }
    },
    handleAdd () {
      this.$dialog(
        EditEvent,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: '新增活动',
          width: '640px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
    },
    handleEdit (record) {
      this.$dialog(
        EditEvent,
        {
          event: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '编辑活动',
          width: '640px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
    },
    handleDelete (record) {
      const that = this
      this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: record.id
          }).then(res => {
            that.$message.success('删除成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
      })
    },
    handleBatchDelete () {
      if (this.selectedRowKeys.length <= 0) {
        this.$message.warn('请勾选删除项')
        return
      }
      const that = this
      this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: that.selectedRowKeys.join(',')
          }).then(res => {
            that.$message.success('删除成功')
            that.selectedRowKeys = []
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
      })
    }
  },
  mounted () {
    this.getList()
  }
}
</script>

<style lang="less" scoped>
.table-wrap {
  flex: 1;
}
.page-view {
  min-height: 100%;
  background: #FFF;
  padding: 24px;
  display: flex;
  flex-direction: column;
}
.table-operation {
  height: 50px;
  text-align: right;
}
</style>
