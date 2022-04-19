<template>
  <el-col>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugOverview' })">
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
    </el-menu>

    <el-table :data="words">
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
import { Back, Check } from "@element-plus/icons-vue";
import { useWordStore } from "@/stores/word";
import { useLabelStore } from "@/stores/label";
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";

export default {
  name: "GlobalSideBar",
  components: {
    Back,
    Check,
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
  created() {
    const promises = [];
    promises.push(this.labelStore.fetchLabels());
    promises.push(this.globalDictionaryStore.fetchDictionary());
    promises.push(this.wordStore.resetState());
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
  computed: {
    words: function () {
      return this.wordStore.getWords;
    },
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
