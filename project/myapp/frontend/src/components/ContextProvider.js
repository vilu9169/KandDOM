import { MessageContextProvider } from "./MessageContextProvider";
import { ResponseContextProvider } from "./ResponseContextProvider";
import { AppProvider } from "./ShowSettingsHandler";
import { DarkModeContextProvider } from "./DarkModeContextProvider";
import { ShowInfoWindowContextProvider } from "./ShowInfoWindowContextProvider";
import { AuthContextProvider } from "./AuthContextProvider";
import { UploadWindowContextProvider } from "./UploadWindowContextProvider";

function ContextProvider({ children }) {
  return (
    <UploadWindowContextProvider>
      <AuthContextProvider>
        <ShowInfoWindowContextProvider>
          <DarkModeContextProvider>
            <ResponseContextProvider>
              <MessageContextProvider>
                <AppProvider>{children}</AppProvider>
              </MessageContextProvider>
            </ResponseContextProvider>
          </DarkModeContextProvider>
        </ShowInfoWindowContextProvider>
      </AuthContextProvider>
    </UploadWindowContextProvider>
  );
}

export default ContextProvider;
