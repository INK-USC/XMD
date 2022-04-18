<template>
  <div>
    <div style="text-align: center">
      <div>
        <h1>All Words in Dictionary</h1>
      </div>
      <el-input
        v-model="searchQuery"
        placeholder="Type to search for words"
        style="width: 50%"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <el-table
      :data="
        dictionaryStore.getRows.filter(
          (row) =>
            !searchQuery ||
            row.word.toLowerCase().includes(searchQuery.toLowerCase().trim())
        )
      "
      stripe
    >
      <el-table-column type="index" :index="indexMethod" />
      <el-table-column label="Text" sortable>
        <template #default="scope">
          <p>{{ scope.row.word }}</p>
        </template>
      </el-table-column>
      <el-table-column
        label="Explanation Type"
        sortable
        :filters="this.filters"
        :filter-method="filterTask"
      >
        <template #default="scope">
          <p>{{ ExplanationTypes[scope.row.explanation_type] }}</p>
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
  </div>
</template>

<script>
import { Search, Delete } from "@element-plus/icons-vue";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";

// show all the document for this project
export default {
  name: "DocumentList",
  components: {
    Search,
    Delete,
  },
  setup() {
    const dictionaryStore = useLocalDictionaryStore();
    const filters = [];
    return {
      dictionaryStore,
      filters,
    };
  },
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    // show the index of the document
    indexMethod(index) {
      return index + 1;
    },
    handleDelete(index, row) {
      this.dictionaryStore.deleteWord(row).then(() => {
        this.dictionaryStore.fetchDictionary();
      });
    },
    filterTask(value, row, column) {
      let taskId = row[column.property];
      let taskName = ExplanationTypes[taskId];
      return value === taskName;
    },
  },
  created() {
    this.dictionaryStore.fetchDictionary();
  },
};
</script>
