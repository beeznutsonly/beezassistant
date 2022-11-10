import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import SinglePageAppViewLayout from "../SinglePageAppViewLayouts/BasicSinglePageAppViewLayout";
import ContentView from "../ContentViews/NavigationSidebarContentView";
import HomeContent from "../NavigableContent/HomeContent";
import ScheduledSubmissionsContent from "../NavigableContent/ScheduledSubmissionsContent";
import ErrorContent from "../NavigableContent/ErrorContent";
import HomeContentView from "../ContentViews/BasicContentView";
import ScheduledCrosspostsContent from "../NavigableContent/ScheduledCrosspostsContent";
import StarsContent from "../NavigableContent/StarsContent";
import ScheduledSubmissionFormDialog from "../NavigableContent/OutletBasedScheduledSubmissionFormDialog";
import ScheduledCrosspostFormDialog from "../NavigableContent/OutletBasedScheduledCrosspostFormDialog";
import StarFormDialog from "../NavigableContent/OutletBasedStarFormDialog";
import AdminUpdateContent from "../NavigableContent/AdminUpdateContent";
import UniversalMediaUrlProcessor from "../../utilities/UniversalMediaUrlProcessor";
import RedGifsMediaUrlProcessor from "../../utilities/RedGifsMediaUrlProcessor";

const BasicSinglePageAppView = () => {

  const apiURL = process.env.NODE_ENV === "development" 
    ? process.env.REACT_APP_DEV_API_URL 
    : process.env.REACT_APP_PROD_API_URL;
    
  const universalMediaUrlProcessor = new UniversalMediaUrlProcessor(
    {
      "redgifs.com": RedGifsMediaUrlProcessor,
      "www.redgifs.com": RedGifsMediaUrlProcessor
    }
  )

  const homeNavigable = {
    "path": "/",
    "linkName": "Home",
    "linkContent": <HomeContent />
  }
  const scheduledSubmissionsNavigable = {
    "path": "/ScheduledSubmissions",
    "linkName": "Scheduled Submissions",
    "linkContent": <ScheduledSubmissionsContent 
        apiURL={apiURL}
        mediaUrlProcessor={universalMediaUrlProcessor}
      />,
    "subNavigables": [
      {
        "path": "add",
        "linkName": "Scheduled Submissions",
        "linkContent": <ScheduledSubmissionFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "add/:itemId",
        "linkName": "Scheduled Submissions",
        "linkContent": <ScheduledSubmissionFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "edit",
        "linkName": "Scheduled Submissions",
        "linkContent": <ScheduledSubmissionFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "edit/:itemId",
        "linkName": "Scheduled Submissions",
        "linkContent": <ScheduledSubmissionFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      }
    ]
  }
  const scheduledCrosspostsNavigable = {
    "path": "/ScheduledCrossposts",
    "linkName": "Scheduled Crossposts",
    "linkContent": <ScheduledCrosspostsContent 
        apiURL={apiURL}
        mediaUrlProcessor={universalMediaUrlProcessor}
      />,
    "subNavigables": [
      {
        "path": "add",
        "linkName": "Scheduled Crossposts",
        "linkContent": <ScheduledCrosspostFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "add/:itemId",
        "linkName": "Scheduled Crossposts",
        "linkContent": <ScheduledCrosspostFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "edit",
        "linkName": "Scheduled Crossposts",
        "linkContent": <ScheduledCrosspostFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor} 
        />
      },
      {
        "path": "edit/:itemId",
        "linkName": "Scheduled Crossposts",
        "linkContent": <ScheduledCrosspostFormDialog
            mediaUrlProcessor={universalMediaUrlProcessor}
        />
      }
    ]
  }
  const starsNavigable = {
    "path": "/Stars",
    "linkName": "Stars",
    "linkContent": <StarsContent 
        apiURL={apiURL}
      />,
    "subNavigables": [
      {
        "path": "add",
        "linkName": "Stars",
        "linkContent": <StarFormDialog />
      },
      {
        "path": "add/:itemId",
        "linkName": "Stars",
        "linkContent": <StarFormDialog />
      },
      {
        "path": "edit",
        "linkName": "Stars",
        "linkContent": <StarFormDialog />
      },
      {
        "path": "edit/:itemId",
        "linkName": "Stars",
        "linkContent": <StarFormDialog />
      }
    ]
  }
  const adminUpdateNavigable = {
    "path": "/AdminUpdate",
    "linkName": "New Admin Update",
    "linkContent": <AdminUpdateContent apiURL={apiURL}/>
  }

  const navigables = [
    homeNavigable, 
    scheduledSubmissionsNavigable,
    scheduledCrosspostsNavigable,
    starsNavigable,
    adminUpdateNavigable
  ];

  const navigationLinks = navigables.map(navigable =>
    ({
      "path": navigable.path,
      "linkName": navigable.linkName
    })
  );

  const unwrapRoute = (navigable, exactPath) => {
    if (navigable.subNavigables) {
      if (exactPath)
        return <Route 
            exact path={navigable.path} 
            element={navigable.linkContent}
            key={navigable.path}
          >
            { unwrapRoutes(navigable.subNavigables, false) }
          </Route>
      return <Route 
        path={navigable.path} 
        element={navigable.linkContent}
        key={navigable.path}
      >
        { unwrapRoutes(navigable.subNavigables, false) }
      </Route>  
    }
    if (exactPath)
        return <Route 
            exact path={navigable.path} 
            element={navigable.linkContent}
            key={navigable.path}
        />
    return <Route 
      path={navigable.path} 
      element={navigable.linkContent}
      key={navigable.path}
    />
  }

  const unwrapRoutes = (navigables, exactPaths) => {
    return navigables.map(navigable => 
      unwrapRoute(navigable, exactPaths)
    );
  }

  return (
    <>
      <Router>
        <Routes>
          <Route exact path="/" element={
            <SinglePageAppViewLayout
              label="Beezassistant Configurator"
              theme="accent"
              navigationLinks={navigationLinks}
            />
          }>
            <Route exact path="/" element={<HomeContentView />}>
              <Route index element={homeNavigable.linkContent} />
            </Route>
            <Route path="/" element={
              <ContentView navigationLinks={navigationLinks}/>
            }>
              {
                unwrapRoutes(navigables, false)
              }
              <Route path="/*" element={<ErrorContent />} />
            </Route>
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default BasicSinglePageAppView;
