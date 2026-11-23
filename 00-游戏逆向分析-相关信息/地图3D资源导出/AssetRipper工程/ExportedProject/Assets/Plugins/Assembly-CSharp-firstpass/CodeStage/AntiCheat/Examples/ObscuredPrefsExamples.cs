using CodeStage.AntiCheat.ObscuredTypes;
using UnityEngine;

namespace CodeStage.AntiCheat.Examples
{
	public class ObscuredPrefsExamples : MonoBehaviour
	{
		private const string PrefsString = "name";

		private const string PrefsInt = "money";

		private const string PrefsFloat = "lifeBar";

		private const string PrefsBool = "gameComplete";

		private const string PrefsUint = "demoUint";

		private const string PrefsLong = "demoLong";

		private const string PrefsDouble = "demoDouble";

		private const string PrefsVector2 = "demoVector2";

		private const string PrefsVector3 = "demoVector3";

		private const string PrefsQuaternion = "demoQuaternion";

		private const string PrefsRect = "demoRect";

		private const string PrefsColor = "demoColor";

		private const string PrefsByteArray = "demoByteArray";

		public string prefsEncryptionKey;

		internal string regularPrefs;

		internal string obscuredPrefs;

		internal bool savesAlterationDetected;

		internal bool foreignSavesDetected;

		internal bool PreservePlayerPrefs
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		internal bool EmergencyMode
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		internal bool ReadForeignSaves
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		private void Awake()
		{
		}

		private void OnDestroy()
		{
		}

		private void SavesAlterationDetected()
		{
		}

		private void ForeignSavesDetected()
		{
		}

		internal void LoadRegularPrefs()
		{
		}

		internal void SaveRegularPrefs()
		{
		}

		internal void DeleteRegularPrefs()
		{
		}

		internal void LockObscuredPrefsToDevice(ObscuredPrefs.DeviceLockLevel level)
		{
		}

		internal void LoadObscuredPrefs()
		{
		}

		internal void SaveObscuredPrefs()
		{
		}

		internal void DeleteObscuredPrefs()
		{
		}
	}
}
