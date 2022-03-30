import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DocumentsApi from "@/utilities/network/document";

export const useDocumentStore = defineStore({
  id: "document",
  state: () => ({
    documents: [],
    curPage: 1,
    maxPage: 1,
    totalDocCount: 0,
    curDocIndex: 0,
    annotatedDocCount: 0,
    pageSize: 10,
  }),
  getters: {
    getDocuments: (state) => {
      return state.documents;
    },
    getdocumentInfo: (state) => {
      return state;
    },
  },
  actions: {
    resetState() {
      this.curPage = 1;
      this.pageSize = 10;
      return this.fetchDocuments();
    },
    setCurDocIndex(curDocIndex) {
      this.curDocIndex = curDocIndex;
    },
    fetchDocuments() {
      const projectStore = useProjectStore();
      return DocumentsApi.list(
        projectStore.getProjectInfo.id,
        this.curPage,
        this.pageSize
      ).then((res) => {
        this.documents = res.results.results;
        this.totalDocCount = res.count;
        this.annotatedDocCount = res.results.annotatedCount;
        this.maxPage = Math.ceil(this.totalDocCount / this.pageSize);
        return res;
      });
    },
    updateCurPage(newPageNum) {
      this.curPage = newPageNum;
      this.curDocIndex = 0;
      return this.fetchDocuments();
    },
    deleteDocument(document) {
      const projectStore = useProjectStore();
      return DocumentsApi.delete(projectStore.getProjectInfo.id, document.id);
    },
    markAnnotated() {
      if (!this.documents[this.curDocIndex].id) return null;
      return DocumentsApi.markAnnotated(
        this.documents[this.curDocIndex].id
      ).then(() => {
        this.document[this.curDocIndex].annotated = true;
      });
    },
  },
});
