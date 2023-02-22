<template>
  <el-col>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugOverview' })">
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
    </el-menu>

    <el-table :data="Array.from(docs)">
      <el-table-column width="40">
        <template #default="scope">
          <span v-if="scope.row.annotated">
            <el-icon><Check /></el-icon>
          </span>
          <div v-else>
            {{
              documentStore.getdocumentInfo.pageSize *
                (documentStore.getdocumentInfo.curPage - 1) +
              scope.$index + 1
            }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="text">
        <template #default="scope">
          <el-link
            @click="goToDocument(scope.$index, scope.row)"
            >{{ this.truncate(scope.row.text, 100) }}
          </el-link>
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
  </el-col>
</template>

<script>
import { Back, Check } from "@element-plus/icons-vue";
import { useDocumentStore } from "@/stores/document";
import { useLabelStore } from "@/stores/label";
import { useDetailedDocumentStore } from "@/stores/detailedDocument";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";

export default {
  name: "LocalSideBar",
  components: {
    Back,
    Check,
  },
  setup() {
    const documentStore = useDocumentStore();
    const detailedDocumentStore = useDetailedDocumentStore();
    const labelStore = useLabelStore();
    const localDictionaryStore = useLocalDictionaryStore();
    return {
      documentStore,
      detailedDocumentStore,
      labelStore,
      localDictionaryStore,
    };
  },
  data() {
    return {
      docs: [],
    };
  },
  created() {
    const promises = [];
    promises.push(this.labelStore.fetchLabels());
    promises.push(
      this.documentStore.resetState().then(() => {
        return this.localDictionaryStore.fetchDictionary(
          this.documentStore.getDocuments[
            this.documentStore.getdocumentInfo.curDocIndex
          ].id
        );
      })
    );
    Promise.all(promises).then(() => {
      this.detailedDocumentStore.fetchDocument(
        this.documentStore.getDocuments[
          this.documentStore.getdocumentInfo.curDocIndex
        ].id
      );
      this.docs = this.documentStore.getDocuments;
      console.log(`updating docs data`);
    });
  },
  methods: {
    pageChanged(pageNum) {
      this.documentStore.updateCurPage(pageNum).then((res) => {
        this.docs = res.results.results;
        console.log(`updating docs data`);
        
        this.detailedDocumentStore.fetchDocument(
          this.documentStore.getDocuments[
            this.documentStore.getdocumentInfo.curDocIndex
          ].id
        );
      });
    },
    goToDocument(index, docInfo) {
      this.documentStore.setCurDocIndex(index);
      this.detailedDocumentStore.fetchDocument(docInfo.id);
      this.localDictionaryStore.fetchDictionary(docInfo.id);
    },
    truncate(text, length) {
          if (text.length > length) {
              return text.substring(0, length) + '...';
          } else {
              return text;
          }
      },
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
