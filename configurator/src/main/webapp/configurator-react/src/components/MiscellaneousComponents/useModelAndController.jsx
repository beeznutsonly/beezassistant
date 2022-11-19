import { observable } from "mobx"

export default function useModelAndController(
    modelClass, controllerClass
) {
    const model = observable(modelClass.defaultModel());
    return {
        model: model,
        controller: new controllerClass(model)
    }
}