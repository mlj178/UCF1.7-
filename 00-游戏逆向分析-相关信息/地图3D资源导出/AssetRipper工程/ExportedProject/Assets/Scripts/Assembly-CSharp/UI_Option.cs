using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.UI;

public class UI_Option : Singleton<UI_Option>
{
	[SerializeField]
	private UI_Tab tab;

	[SerializeField]
	private Dropdown dpd_Resolution;

	[SerializeField]
	private UI_SelectionGroup fullScreenSwitch;

	[SerializeField]
	private Slider mouseSpeed;

	[SerializeField]
	private Slider zoomSpeed;

	[SerializeField]
	private AudioMixer audioMixer;

	[SerializeField]
	private UI_SelectionGroup bgmSwitch;

	[SerializeField]
	private Slider bgmSlider;

	[SerializeField]
	private UI_SelectionGroup sndSwitch;

	[SerializeField]
	private Slider sndSlider;

	[SerializeField]
	private UI_SelectionGroup radioSwitch;

	[SerializeField]
	private Slider radioSlider;

	private static Vector2Int[] resolutions;

	private void Start()
	{
	}

	public void OnCancelBtnDown()
	{
	}

	public void OnBgmSwitchValueChange(int value)
	{
	}

	public void OnBgmSliderValueChange(float value)
	{
	}

	public void OnSndSwitchValueChange(int value)
	{
	}

	public void OnSndSliderValueChange(float value)
	{
	}

	public void OnRadioSwitchValueChange(int value)
	{
	}

	public void OnRadioSliderValueChange(float value)
	{
	}

	private float CalculateAudioVolume(float value)
	{
		return 0f;
	}

	private void UpdateUI()
	{
	}

	public void OnSaveBtnDown()
	{
	}

	public override void SetVisible(bool visible)
	{
	}

	private void SetResolution()
	{
	}

	private void SetMouseSpeed()
	{
	}
}
