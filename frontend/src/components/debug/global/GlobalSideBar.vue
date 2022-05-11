<template>
  <el-col>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugOverview' })">
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
    </el-menu>

    <el-input
      v-model="searchQuery"
      placeholder="Type to search for words"
      style="margin-top: 20px; width: 90%"
      clearable
    >
      <template #prefix>
        <div style="align-content: center">
          <el-icon><Search /></el-icon>
        </div>
      </template>
    </el-input>
    <el-table :data="Array.from(wordStore.getWords)">
      <el-table-column width="40">
        <template #default="scope">
          <span v-if="globalDictionaryStore.containsWord(scope.row.text)">
            <el-icon><Check /></el-icon>
          </span>
          <div v-else>
            {{
              wordStore.getWordInfo.pageSize *
                (wordStore.getWordInfo.curPage - 1) +
              scope.$index +
              1
            }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="text">
        <template #default="scope">
          <el-link
            :key="scope.row.text"
            v-snip="{ lines: 3 }"
            @click="goToDocument(scope.$index)"
            >{{ scope.row.text }}</el-link
          >
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      background
      layout="prev, pager, next"
      :total="wordStore.getWordInfo.totalWordCount"
      :page-size="wordStore.getWordInfo.pageSize"
      :current-page="wordStore.getWordInfo.curPage"
      @current-change="pageChanged"
      style="text-align: center"
    />
  </el-col>
</template>

<script>
import { Back, Check, Search } from "@element-plus/icons-vue";
import { useWordStore } from "@/stores/word";
import { useLabelStore } from "@/stores/label";
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";

export default {
  name: "GlobalSideBar",
  components: {
    Back,
    Check,
    Search,
  },
  setup() {
    const labelStore = useLabelStore();
    const wordStore = useWordStore();
    const globalDictionaryStore = useGlobalDictionaryStore();
    return {
      labelStore,
      wordStore,
      globalDictionaryStore,
    };
  },
  data() {
    return {
      searchQuery: "",
    };
  },
  watch: {
    searchQuery: function (newSearchQuery, oldSearchQuery) {
      console.log(newSearchQuery);
      if (newSearchQuery === "")
        this.wordStore.resetState().then(() => {
          this.wordStore.fetchDocuments();
        });
      else
        this.wordStore.resetState(newSearchQuery).then(() => {
          this.wordStore.fetchDocuments();
        });
    },
  },
  created() {
    if (this.$route.query.q !== undefined) {
      this.searchQuery = this.$route.query.q;
    }
    const promises = [];
    promises.push(this.labelStore.fetchLabels());
    promises.push(this.globalDictionaryStore.fetchDictionary());

    if (this.searchQuery === "") promises.push(this.wordStore.resetState());
    else promises.push(this.wordStore.resetState(this.searchQuery));

    Promise.all(promises).then(() => {
      this.wordStore.fetchDocuments();
    });
  },
  methods: {
    pageChanged(pageNum) {
      this.wordStore.updateCurPage(pageNum).then(() => {
        this.wordStore.fetchDocuments();
      });
    },
    goToDocument(index) {
      this.wordStore.setCurWordIndex(index);
      this.wordStore.fetchDocuments();
    },
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
