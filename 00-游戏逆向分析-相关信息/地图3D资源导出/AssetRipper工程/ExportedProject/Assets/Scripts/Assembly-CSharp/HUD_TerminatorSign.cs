using UnityEngine;
using UnityEngine.UI;

public class HUD_TerminatorSign : MonoBehaviour
{
	[SerializeField]
	private Button readBtn;

	[SerializeField]
	private Text btnText;

	[SerializeField]
	private Text centerText;

	private int curText;

	private string[] myTexts;

	private void Awake()
	{
	}

	private void Start()
	{
	}

	public void NextRead()
	{
	}
}
