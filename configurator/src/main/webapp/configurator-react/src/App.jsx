import { BrowserRouter as Router } from "react-router-dom";

import AppView from "./components/AppViews/BasicAppView";
import NonRootContentView from "./components/ContentViews/NavigationSidebarContentView";
import HomeContent from "./components/NavigableContent/HomeContent";
import ScheduledSubmissionsContent from "./components/NavigableContent/ScheduledSubmissionsContent";
import RootContentView from "./components/ContentViews/BasicContentView";
import ScheduledCrosspostsContent from "./components/NavigableContent/ScheduledCrosspostsContent";
import StarsContent from "./components/NavigableContent/StarsContent";
import ScheduledSubmissionFormDialog from "./components/NavigableContent/OutletBasedScheduledSubmissionFormDialog";
import ScheduledCrosspostFormDialog from "./components/NavigableContent/OutletBasedScheduledCrosspostFormDialog";
import StarFormDialog from "./components/NavigableContent/OutletBasedStarFormDialog";
import AdminUpdateContent from "./components/NavigableContent/AdminUpdateContent";
import UniversalMediaUrlProcessor from "./utilities/UniversalMediaUrlProcessor";
import RedGifsMediaUrlProcessor from "./utilities/RedGifsMediaUrlProcessor";
import { useState } from "react";
import AppRouteConstructor from "./components/MiscellaneousComponents/AppRouteConstructor";

const App = () => {
  const [theme] = useState("accent");
  const itemApiUrl =
    process.env.NODE_ENV === "development"
      ? process.env.REACT_APP_DEV_API_URL
      : process.env.REACT_APP_PROD_API_URL;

  const universalMediaUrlProcessor = new UniversalMediaUrlProcessor({
    "redgifs.com": RedGifsMediaUrlProcessor,
    "www.redgifs.com": RedGifsMediaUrlProcessor,
  });

  const homeNavigable = {
    path: "/",
    linkName: "Home",
    linkContent: <HomeContent />,
  };

  const scheduledSubmissionFormDialog = (
    <ScheduledSubmissionFormDialog
      mediaUrlProcessor={universalMediaUrlProcessor}
    />
  );
  const scheduledSubmissionsNavigable = {
    path: "/ScheduledSubmissions",
    linkName: "Scheduled Submissions",
    linkContent: (
      <ScheduledSubmissionsContent
        apiURL={itemApiUrl}
        mediaUrlProcessor={universalMediaUrlProcessor}
      />
    ),
    subNavigables: [
      {
        path: "add",
        linkName: "Scheduled Submissions",
        linkContent: scheduledSubmissionFormDialog,
      },
      {
        path: "add/:itemId",
        linkName: "Scheduled Submissions",
        linkContent: scheduledSubmissionFormDialog,
      },
      {
        path: "edit",
        linkName: "Scheduled Submissions",
        linkContent: scheduledSubmissionFormDialog,
      },
      {
        path: "edit/:itemId",
        linkName: "Scheduled Submissions",
        linkContent: scheduledSubmissionFormDialog,
      },
    ],
  };

  const scheduledCrosspostFormDialog = (
    <ScheduledCrosspostFormDialog
      apiURL={itemApiUrl}
      mediaUrlProcessor={universalMediaUrlProcessor}
    />
  );
  const scheduledCrosspostsNavigable = {
    path: "/ScheduledCrossposts",
    linkName: "Scheduled Crossposts",
    linkContent: <ScheduledCrosspostsContent apiURL={itemApiUrl} />,
    subNavigables: [
      {
        path: "add",
        linkName: "Scheduled Crossposts",
        linkContent: scheduledCrosspostFormDialog,
      },
      {
        path: "add/:itemId",
        linkName: "Scheduled Crossposts",
        linkContent: scheduledCrosspostFormDialog,
      },
      {
        path: "edit",
        linkName: "Scheduled Crossposts",
        linkContent: scheduledCrosspostFormDialog,
      },
      {
        path: "edit/:itemId",
        linkName: "Scheduled Crossposts",
        linkContent: scheduledCrosspostFormDialog,
      },
    ],
  };

  const starFormDialog = <StarFormDialog />;
  const starsNavigable = {
    path: "/Stars",
    linkName: "Stars",
    linkContent: <StarsContent apiURL={itemApiUrl} />,
    subNavigables: [
      {
        path: "add",
        linkName: "Stars",
        linkContent: starFormDialog,
      },
      {
        path: "add/:itemId",
        linkName: "Stars",
        linkContent: starFormDialog,
      },
      {
        path: "edit",
        linkName: "Stars",
        linkContent: starFormDialog,
      },
      {
        path: "edit/:itemId",
        linkName: "Stars",
        linkContent: starFormDialog,
      },
    ],
  };

  const adminUpdateNavigable = {
    path: "/AdminUpdate",
    linkName: "New Admin Update",
    linkContent: <AdminUpdateContent apiURL={itemApiUrl} />,
  };

  const navigables = [
    homeNavigable,
    scheduledSubmissionsNavigable,
    scheduledCrosspostsNavigable,
    starsNavigable,
    adminUpdateNavigable,
  ];

  const navigationLinks = navigables.map((navigable) => ({
    path: navigable.path,
    linkName: navigable.linkName,
  }));

  const appView = (
    <AppView
      title="Beezassistant Configurator"
      theme={theme}
      navigationLinks={navigationLinks}
    />
  );
  const rootContentView = <RootContentView />;
  const nonRootContentView = (
    <NonRootContentView navigationLinks={navigationLinks} />
  );

  return (
    <>
      <Router>
        <AppRouteConstructor
          appView={appView}
          rootContentView={rootContentView}
          nonRootContentView={nonRootContentView}
          homeNavigable={homeNavigable}
          navigables={navigables}
        />
      </Router>
    </>
  );
};

export default App;
