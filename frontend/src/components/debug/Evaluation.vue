<template>
    <el-row style="width: 100%">
        <el-card style="width: 100%;">
            <template #header>
                <h3>Evaluation Section</h3>
            </template>
            <el-row>
                <span>Model Selected: <b>debugmodel_proj1.h5</b></span>

                <el-divider />
                <h4>Example Input</h4>
                <el-form :model="exampleInputsForm" size="large" style="width: 100%">
                    <el-form-item>
                        <el-select v-model="exampleInputsForm.sentence_id" placeholder="Select a Sentence" size="large"
                            style="width: 100%;">
                            <el-option  
                                v-for="doc in documentStore.getDocuments"
                                :key="doc.id"
                                :label="doc.text"
                                :value="doc.id"
                            />
                        </el-select>
                    </el-form-item>

                </el-form>

                <div>
                    <h4 style="margin-top: 4em;">Attribution scores</h4>
                    <div>
                        <span><span
                                style="display: inline-block; width: 8em; text-align: left; font-style: italic;">Original</span>:
                            All muslims are terrorists and need to be deported from this country</span>
                    </div>
                    <div>
                        <span> <span
                                style="display: inline-block; width: 8rem; text-align: left; font-style: italic;">Debugged
                                Text</span>: All muslims are terrorists and need to be deported from this country</span>
                    </div>
                </div>

                <div v-if="exampleInputsForm.sentence_id">
                    <!-- test: {{ getDocText }} -->
                </div>
                


            </el-row>
        </el-card>
    </el-row>
</template>

<script>
import { Back, Check } from "@element-plus/icons-vue";
import { useDocumentStore } from "@/stores/document";
import { useLabelStore } from "@/stores/label";
import { useDetailedDocumentStore } from "@/stores/detailedDocument";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";

export default {
    name: "DebugEvaluation",
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
        });
    },
    data() {
        return {
            exampleInputsForm: {
                sentence_id: ""
            }
        }
    },
    computed: {
        getDocText() {
            console.log("calling getDocTest")
            console.log(this.exampleInputsForm.sentence_id)
            this.detailedDocumentStore.fetchDocument(this.exampleInputsForm.sentence_id)
            return this.detailedDocumentStore.getDocument
        }
    },
};


</script>