<template>
  <div>
    <div style="text-align: center">
      <div>
        <h1>All Uploaded Documents</h1>
        <!-- <el-progress
          type="circle"
          width=180 
          :percentage="percentageCompleted"
          :format="percentageText"
        /> -->
      </div>
      <el-input
        v-model="searchQuery"
        placeholder="Type to search for documents"
        style="width: 50%"
        clearable
      >
        <template #prefix>
          <div style="align-content: center">
            <el-icon><Search /></el-icon>
          </div>
        </template>
      </el-input>
    </div>

    <el-table
      :data="
        documentStore.getDocuments.filter(
          (row) =>
            !searchQuery ||
            row.text.toLowerCase().includes(searchQuery.toLowerCase().trim())
        )
      "
      stripe
    >
      <el-table-column type="index" :index="indexMethod" />
      <el-table-column prop="text" label="Text">
        <template #default="scope">
          {{ scope.row.text }}
        </template>
      </el-table-column>
      <el-table-column label="Operations">
        <template #default="scope">
          <el-popconfirm
            title="Are you sure?"
            @confirm="handleDelete(scope.$index, scope.row)"
            style="margin-left: 10px"
          >
            <template #reference>
              <el-button size="small" type="danger"
                ><el-icon><Delete /></el-icon>Delete</el-button
              >
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      layout="prev, pager, next"
      :total="documentStore.getdocumentInfo.totalDocCount"
      :page-size="documentStore.getdocumentInfo.pageSize"
      :current-page="documentStore.getdocumentInfo.curPage"
      @current-change="pageChanged"
      style="text-align: center"
    />
  </div>
  <WorkflowTutorial
    v-model:dialog-visible="tutorialVisible"
  />
</template>

<script>
import { Search, Delete, QuestionFilled } from "@element-plus/icons-vue";
import { useDocumentStore } from "@/stores/document";
import WorkflowTutorial from "@/components/project/tutorial/WorkflowTutorial.vue";

// show all the document for this project
export default {
  name: "DocumentList",
  components: {
    WorkflowTutorial,
    Search,
    Delete,
    QuestionFilled,
  },
  setup() {
    const documentStore = useDocumentStore();
    return {
      documentStore,
    };
  },
  data() {
    return {
      tutorialVisible: true,
      searchQuery: "",
    };
  },
  methods: {
    // go to selected page
    pageChanged(pageNum) {
      this.documentStore.updateCurPage(pageNum);
    },
    // show the index of the document
    indexMethod(index) {
      return index + 1;
    },
    // show the percentage of annotated document
    percentageText(percentage) {
      return `${percentage} % annotated`;
    },
    handleDelete(index, row) {
      this.documentStore.deleteDocument(row).then(() => {
        this.documentStore.fetchDocuments();
      });
    },
  },
  created() {
    this.documentStore.resetState();
  },
  // filters: {
  //   truncate(text, length) {
  //       console.log(text.length)
  //       if (text.length > length) {
  //           return text.substring(0, length) + '...';
  //       } else {
  //           return text;
  //       }
  //   }
  // }
  // computed: {
  //   percentageCompleted() {
  //     const info = this.documentStore.getdocumentInfo;
  //     if (!info) {
  //       return 0;
  //     }
  //     const completed = info.annotatedDocCount;
  //     const all = info.totalDocCount;
  //     const percent = (completed / all) * 100;
  //     return percent ? percent : 0;
  //   },
  // },
};
</script>
