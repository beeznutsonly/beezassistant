import ContentShard from "../ContentShards/StandardContentShard";
import AlertSystem from "../../utilities/AlertSystem";
import React, { useCallback, useEffect, useState } from "react";
import AlertContainer from "../Alerts/AlertContainer";
import ConfirmationDialog from "../ConfirmationDialogs/ConfirmationDialog";
import AlertModel from "../../models/AlertModel";
import ConfirmationDialogModel from "../../models/ConfirmationDialogModel";
import LoadingAnimation from "../LoadingAnimations/BasicInlineLoadingAnimation";
import LoadingAnimationModel from "../../models/InlineLoadingAnimationModel";
import OutletInputBasedEditableList from "../Lists/EditableList/OutletInputBasedEditableList";
import ItemManipulationTools, { ItemTools } from "../Forms/ItemManipulationTools";
import { delay } from "../../utilities/GeneralUtilities";

const OutletBasedEditableListContent = (props) => {

    const itemsRepository = props.itemsRepository;
    const [items, setItems] = useState([]);

    const [confirmationDialogModel, setConfirmationDialogModel] = useState(
      ConfirmationDialogModel.defaultConfirmationDialogModel()
    );
    const [alertModel, setAlertModel] = useState(
      AlertModel.defaultAlertModel()
    );
    const [loadingAnimationModel, setLoadingAnimationModel] = useState(
      LoadingAnimationModel.defaultLoadingAnimationModel()
    )
    const confirmationDialog = <ConfirmationDialog 
      confirmationDialogState={[confirmationDialogModel, setConfirmationDialogModel]}
    />
    const alertContainer = <AlertContainer 
      alertState={[alertModel, setAlertModel]}
    />
    const loadingAnimation = <LoadingAnimation
      loadingAnimationModel={loadingAnimationModel} 
    />
    
    const [isRefreshing, setRefreshing] = useState(false);
    const [isAdding, setAdding] = useState(false);
    const [isEditing, setEditing] = useState(false);
    const [isRemoving, setRemoving] = useState(false);
    
    const alertSystem = useState(new AlertSystem(
        setAlertModel, 
        setConfirmationDialogModel
    ))[0];

    const retrieveItems = useCallback(() => {
        const promise = itemsRepository.retrieveItems();
        return promise.then((response) => {
            if (response.ok) {
                return response.json();
            }
            else {
                return Promise.reject(new Error(response.status))
            }
        })
        .then(responseJson => {
            return Object.values(responseJson._embedded)[0]
        }) 
    }, [itemsRepository])

    // const addItem = (itemModel) => {
    //     const promise = itemsRepository.addItem(itemModel);
    //     return promise.then((response) => {
    //         if (!response.ok) {
    //             return Promise.reject(new Error(response.status))
    //         }
    //         return response.json();
    //     })
    // }

    // const editItem = (updatedItem) => {
    //     const promise = itemsRepository.editItem(updatedItem);
    //     return promise.then((response) => {
    //         if (!response.ok) {
    //             return Promise.reject(new Error(response.status))
    //         }
    //         return response.json();
    //     });
    // }

    const removeItem = (item) => {
        const promise = itemsRepository.removeItem(item);
        return promise.then((response) => {
            if (!response.ok) {
                return Promise.reject(new Error(response.status))
            }
            return response;
        });
    }

    const removeItems = (items) => {
        return new Promise((resolveOuter) => {
            const innerPromise = new Promise((resolve) => resolve())
            items.forEach(item => {
                innerPromise.then(() => removeItem(item))
            });
            resolveOuter();
        });       
    }

    const __actionHandlerStub = useCallback((actionHandler, statusSetter, successCallback) => {
        statusSetter(true);
        actionHandler()
            .then((payload) => {
                successCallback(payload);
            })
            .catch((error) => {
                const errorMessage = `Could not complete the task: ${error}`;
                alertSystem.alert(
                    errorMessage, "danger", false, "An error occurred"
                )
                console.error(
                    errorMessage
                );
            })
            .finally(() => {
                statusSetter(false);
            });
    }, [alertSystem]);

    const refreshItemsHandler = useCallback(() => {
        alertSystem.closeAlert();
        __actionHandlerStub(
            () => retrieveItems(),
            setRefreshing,
            (retrievedItems) => {
                setItems(retrievedItems);
            }
        );
    }, [__actionHandlerStub, alertSystem, retrieveItems]);

    const addItemSuccessCallback = (addedItem) => {
        if (!items.includes(addedItem))
            setItems(
                [...items, addedItem]
            );
        alertSystem.alert(
            `Item successfully added`,
            'success',
            true
        );
        delay(4000, () => refreshItemsHandler());
    }

    const editItemSuccessCallback = (updatedItem) => {
        const filteredItems = items.filter((item) => 
            item._links.self.href !== updatedItem._links.self.href
        );
        setItems(
            [...filteredItems, updatedItem]
        );
        alertSystem.alert(
            `Item successfully edited`,
            'success',
            true
        );
        delay(4000, () => refreshItemsHandler());
    }

    const removeItemsHandler = (itemsToBeRemoved) => {
        __actionHandlerStub(
            () => removeItems(itemsToBeRemoved),
            setRemoving,
            () => {
                setItems(
                    items.filter(
                        item => !itemsToBeRemoved.has(item)
                    )
                );
                alertSystem.alert(
                    `${
                        itemsToBeRemoved.size === 1 
                        ? 'Item' 
                        : 'Items'
                    } successfully removed`,
                    'success',
                    true
                );
                delay(4000, () => refreshItemsHandler());
            }
        );
    }

    const removeSelectedHandler = (itemsToBeRemoved) => {
        alertSystem.confirm(
            'Are you sure you want to remove ' +
            'the selected item(s)?',
            () => removeItemsHandler(itemsToBeRemoved)
        );
    }

    useEffect(() => {
        setLoadingAnimationModel(
            {
            ...loadingAnimationModel,
            isShown: isRefreshing || 
                isAdding || 
                isEditing ||   
                isRemoving
            }
        );
    }, [isRefreshing, isAdding, isEditing, isRemoving, loadingAnimationModel])

    useEffect(() => {
        refreshItemsHandler();
    }, [refreshItemsHandler])
  
    return (
      <>
        <ContentShard
           title={props.shardTitle} 
           alertContainer={alertContainer}
           loadingAnimation={loadingAnimation}
        >
          {confirmationDialog}
          <OutletInputBasedEditableList
            items={items}
            sortingFunctions={props.sortingFunctions}
            itemMappingFunction={props.itemMappingFunction}
            itemManipulationTools={
              new ItemManipulationTools(
                itemsRepository,
                new ItemTools(addItemSuccessCallback, [isAdding, setAdding]),
                new ItemTools(editItemSuccessCallback, [isEditing, setEditing])
              )
            }
            refreshItemsHandler={refreshItemsHandler}
            removeSelectedHandler={removeSelectedHandler}
            actionStatuses={{
              isRefreshing: isRefreshing,
              isAdding: isAdding,
              isEditing: isEditing,
              isRemoving: isRemoving
            }}
          />
        </ContentShard>
      </>
    );
  }

export default OutletBasedEditableListContent;