using CodeStage.AntiCheat.ObscuredTypes;
using UnityEngine;

namespace CodeStage.AntiCheat.Examples
{
	public class ExamplesGUI : MonoBehaviour
	{
		private enum ExamplePage
		{
			ObscuredTypes = 0,
			ObscuredPrefs = 1,
			Detectors = 2
		}

		private const string RedColor = "#FF4040";

		private const string YellowColor = "#E9D604";

		private const string GreenColor = "#02C85F";

		public ObscuredTypesExamples obscuredTypesExamples;

		public ObscuredPrefsExamples obscuredPrefsExamples;

		public DetectorsExamples detectorsExamples;

		private readonly string[] tabs;

		private ExamplePage currentPage;

		private string allSimpleObscuredTypes;

		private ObscuredPrefs.DeviceLockLevel savesLock;

		private GUIStyle centeredStyle;

		private void OnGUI()
		{
		}

		private void DrawObscuredTypesPage()
		{
		}

		private void DrawObscuredPrefsPage()
		{
		}

		private void DrawDetectorsPage()
		{
		}

		private string GetAllSimpleObscuredTypes()
		{
			return null;
		}

		private string GetAllObscuredPrefsDataTypes()
		{
			return null;
		}
	}
}
