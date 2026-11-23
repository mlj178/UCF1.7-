using System;
using System.Collections.Generic;
using UnityEngine;

public class INIParser
{
	public int error;

	private object m_Lock;

	private string m_FileName;

	private string m_iniString;

	private bool m_AutoFlush;

	private Dictionary<string, Dictionary<string, string>> m_Sections;

	private Dictionary<string, Dictionary<string, string>> m_Modified;

	private bool m_CacheModified;

	public string FileName => null;

	public string iniString => null;

	public void Open(string path)
	{
	}

	public void Open(TextAsset name)
	{
	}

	public void OpenFromString(string str)
	{
	}

	public override string ToString()
	{
		return null;
	}

	private void Initialize(string iniString, bool AutoFlush)
	{
	}

	public void Close()
	{
	}

	private string ParseSectionName(string Line)
	{
		return null;
	}

	private bool ParseKeyValuePair(string Line, ref string Key, ref string Value)
	{
		return false;
	}

	private bool isComment(string Line)
	{
		return false;
	}

	private void Refresh()
	{
	}

	private void PerformFlush()
	{
	}

	public bool IsSectionExists(string SectionName)
	{
		return false;
	}

	public bool IsKeyExists(string SectionName, string Key)
	{
		return false;
	}

	public void SectionDelete(string SectionName)
	{
	}

	public void KeyDelete(string SectionName, string Key)
	{
	}

	public string ReadValue(string SectionName, string Key, string DefaultValue)
	{
		return null;
	}

	public void WriteValue(string SectionName, string Key, string Value)
	{
	}

	private string EncodeByteArray(byte[] Value)
	{
		return null;
	}

	private byte[] DecodeByteArray(string Value)
	{
		return null;
	}

	public bool ReadValue(string SectionName, string Key, bool DefaultValue)
	{
		return false;
	}

	public int ReadValue(string SectionName, string Key, int DefaultValue)
	{
		return 0;
	}

	public long ReadValue(string SectionName, string Key, long DefaultValue)
	{
		return 0L;
	}

	public double ReadValue(string SectionName, string Key, double DefaultValue)
	{
		return 0.0;
	}

	public byte[] ReadValue(string SectionName, string Key, byte[] DefaultValue)
	{
		return null;
	}

	public DateTime ReadValue(string SectionName, string Key, DateTime DefaultValue)
	{
		return default;
	}

	public void WriteValue(string SectionName, string Key, bool Value)
	{
	}

	public void WriteValue(string SectionName, string Key, int Value)
	{
	}

	public void WriteValue(string SectionName, string Key, long Value)
	{
	}

	public void WriteValue(string SectionName, string Key, double Value)
	{
	}

	public void WriteValue(string SectionName, string Key, byte[] Value)
	{
	}

	public void WriteValue(string SectionName, string Key, DateTime Value)
	{
	}
}
