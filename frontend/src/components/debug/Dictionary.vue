<template>
  <div>
    <div style="text-align: center">
      <div>
        <h1>All Words in Global Dictionary</h1>
      </div>
      <el-input
        v-model.lazy.trim="searchQuery"
        placeholder="Type to search for words"
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

    <el-table :data="Array.from(dictionaryStore.getRows)" stripe>
      <el-table-column type="index" :index="indexMethod" />
      <el-table-column label="Text" sortable>
        <template #default="scope">
          <p @click="onClick(scope.$index, scope.row)" style="cursor: pointer">
            {{ scope.row.word }}
          </p>
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
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";

export default {
  name: "DictionaryOverview",
  components: {
    Search,
    Delete,
  },
  setup() {
    const dictionaryStore = useGlobalDictionaryStore();
    return {
      dictionaryStore,
    };
  },
  data() {
    return {
      searchQuery: "",
    };
  },
  watch: {
    searchQuery: function (newSearchQuery, oldSearchQuery) {
      this.dictionaryStore.fetchDictionary(newSearchQuery);
    },
  },
  methods: {
    // show the index of the document
    indexMethod(index) {
      return index + 1;
    },
    onClick(index, row) {
      this.$router.push({ name: "DebugGlobal", query: { q: row.word } });
    },
    handleDelete(index, row) {
      this.dictionaryStore.deleteWord(row.word).then(() => {
        this.dictionaryStore.fetchDictionary();
      });
    },
  },
  created() {
    this.dictionaryStore.fetchDictionary();
  },
};
</script>
